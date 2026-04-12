"""
agents/threads_notifier.py

KDP本の生成完了後にThreadsへ告知投稿を行う。
けんた（AI時短サラリーマン）アカウントで「AIで本を書いてみた」系の投稿を自動生成。

config.json に以下を追加することで有効化:
  "threads_notify": {
    "enabled": true,
    "account_id": "account_c",
    "access_token": "YOUR_LONG_LIVED_TOKEN",
    "threads_user_id": "YOUR_THREADS_USER_ID"
  }
"""

from __future__ import annotations

import json
import logging
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Optional

try:
    import anthropic as _anthropic_module
    _client: Optional[Any] = (
        _anthropic_module.Anthropic() if os.environ.get("ANTHROPIC_API_KEY") else None
    )
except ImportError:
    _client = None

THREADS_API_BASE = "https://graph.threads.net/v1.0"

NOTIFY_PROMPT = """
あなたは「AI時短サラリーマン けんた」というThreadsアカウントの中の人です。

【けんたのキャラクター】
- 32歳、都内勤務の会社員
- AIを使いこなして定時退社・副業月3万達成
- 親しみやすい・タメ語と敬語の中間のトーン
- 実際の体験・数字を具体的に話す

以下のKDP本を生成しました。この本をThreadsで告知する投稿文（本文）とリプライ文を作ってください。

【本の情報】
タイトル: {title}
文字数: {total_chars:,}字
価格: {price}円
生成にかかった時間: 約{generation_minutes}分（AIが自動生成）
キーワード: {keywords}

【投稿ルール】
- 本文: 150〜250字。「AIで本を書いてKDPに出してみた」という実験報告のトーン
- 数字（文字数・価格・時間）を必ず入れる
- 最後に「▼詳しくは返信欄へ」で締める
- リプライ: 200〜300字。どんな内容の本か、誰向けか、Claude/AIをどう使ったかを具体的に
- リプライの最後に「まず1冊、試してみて☝️」で締める

以下のJSON形式のみで返してください：
{{
  "body": "本文テキスト",
  "reply": "リプライテキスト"
}}
"""


def _threads_api_call(user_id: str, access_token: str, text: str, reply_to_id: Optional[str] = None) -> str:
    """Threads APIでテキスト投稿を作成してIDを返す。"""
    # Step1: コンテナ作成
    params: dict = {
        "media_type": "TEXT",
        "text": text,
        "access_token": access_token,
    }
    if reply_to_id:
        params["reply_to_id"] = reply_to_id

    create_url = f"{THREADS_API_BASE}/{user_id}/threads"
    data = json.dumps(params).encode("utf-8")
    req = urllib.request.Request(create_url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        container_id = json.loads(resp.read().decode())["id"]

    # Step2: 公開
    publish_url = f"{THREADS_API_BASE}/{user_id}/threads_publish"
    pub_params = {"creation_id": container_id, "access_token": access_token}
    pub_data = json.dumps(pub_params).encode("utf-8")
    req2 = urllib.request.Request(publish_url, data=pub_data, method="POST")
    req2.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req2, timeout=30) as resp2:
        post_id = json.loads(resp2.read().decode())["id"]

    return post_id


def generate_post_text(book_entry: dict, generation_minutes: int = 15) -> Optional[dict]:
    """Claude Haikuで告知投稿文を生成する。"""
    if _client is None:
        return None

    meta = book_entry.get("kdp_metadata", {})
    prompt = NOTIFY_PROMPT.format(
        title=book_entry.get("title", ""),
        total_chars=book_entry.get("total_chars", 0),
        price=meta.get("price_jpy", 980),
        generation_minutes=generation_minutes,
        keywords=", ".join(meta.get("keywords", [])[:4]),
    )

    try:
        response = _client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        text = next((b.text for b in response.content if b.type == "text"), "")
        import re
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if not match:
            return None
        raw = re.sub(r',\s*([}\]])', r'\1', match.group())
        return json.loads(raw)
    except Exception as e:
        logging.error(f"投稿文生成失敗: {e}")
        return None


def notify(book_entry: dict, config: dict, generation_minutes: int = 15, dry_run: bool = False) -> bool:
    """
    KDP本の生成完了をThreadsに告知する。

    Args:
        book_entry: book_history.jsonの1エントリ
        config:     KDP config.json の内容
        generation_minutes: 生成にかかった分数（目安）
        dry_run:    Trueなら実際に投稿せずログ出力のみ

    Returns:
        成功したらTrue
    """
    notify_cfg = config.get("threads_notify", {})
    if not notify_cfg.get("enabled", False):
        logging.info("[threads_notifier] threads_notify.enabled=false のためスキップ")
        return False

    access_token = notify_cfg.get("access_token", "")
    user_id = notify_cfg.get("threads_user_id", "")
    if not access_token or not user_id:
        logging.warning("[threads_notifier] access_token または threads_user_id が未設定")
        return False

    logging.info("[threads_notifier] 告知投稿文を生成中...")
    post = generate_post_text(book_entry, generation_minutes)
    if not post:
        logging.error("[threads_notifier] 投稿文生成失敗")
        return False

    body = post.get("body", "")
    reply = post.get("reply", "")
    logging.info(f"[threads_notifier] 本文:\n{body}")
    logging.info(f"[threads_notifier] リプライ:\n{reply}")

    if dry_run:
        logging.info("[threads_notifier] dry_run=true のため投稿スキップ")
        return True

    try:
        post_id = _threads_api_call(user_id, access_token, body)
        logging.info(f"[threads_notifier] 本文投稿完了: {post_id}")
        time.sleep(45)
        reply_id = _threads_api_call(user_id, access_token, reply, reply_to_id=post_id)
        logging.info(f"[threads_notifier] リプライ投稿完了: {reply_id}")
        return True
    except Exception as e:
        logging.error(f"[threads_notifier] 投稿失敗: {e}")
        return False
