"""
agents/researcher.py

Amazon KDP日本語市場で売れやすいテーマを調査し、
候補リストをresearch_cache/に保存する。

使用モデル: claude-haiku-4-5（コスト最小化）
"""

from __future__ import annotations

import json
import logging
import os
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Optional

try:
    import anthropic as _anthropic_module
    _client: Optional[Any] = (
        _anthropic_module.Anthropic() if os.environ.get("ANTHROPIC_API_KEY") else None
    )
except ImportError:
    _client = None

BASE_DIR = Path(__file__).parent.parent
RESEARCH_CACHE_DIR = BASE_DIR / "research_cache"
LOG_PATH = BASE_DIR / "logs" / "researcher.log"
JST = timezone(timedelta(hours=9))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def setup_file_logging() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logging.getLogger().addHandler(handler)


def save_json(path: Path, data: Any) -> None:
    tmp = path.with_suffix(".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        tmp.replace(path)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise


RESEARCH_PROMPT = """
あなたはAmazon KDP（Kindle Direct Publishing）の日本語市場に精通した
出版コンサルタントです。

現在（{date}）、日本語Amazon KDPで売れやすい電子書籍のテーマを8つ提案してください。

【選定基準】
- 日本語市場での需要が高い（検索ボリューム・関心が高い）
- 競合が多すぎず、新規参入の余地がある
- 50〜100ページ程度の実用書・ハウツー本として成立する
- 時流に乗っているが、数年間は需要が続く
- ジャンルは問わない（ビジネス・健康・趣味・人間関係・節約・AI活用など何でも可）

【出力形式】JSON形式のみで返すこと。

{{
  "researched_at": "{date}",
  "candidates": [
    {{
      "title": "本のタイトル案（具体的で魅力的なもの）",
      "subtitle": "サブタイトル案",
      "genre": "ジャンル（ビジネス/健康/趣味/人間関係/マネー/自己啓発/その他）",
      "target_reader": "ターゲット読者層（具体的に）",
      "core_problem": "この本が解決する読者の悩みや課題",
      "key_selling_point": "なぜこの本が売れるか（差別化ポイント）",
      "estimated_chapters": ["章タイトル1", "章タイトル2", "章タイトル3", "章タイトル4", "章タイトル5"],
      "market_timing": "今このテーマが売れやすい理由"
    }}
  ]
}}
"""


def research_topics() -> Optional[dict]:
    if _client is None:
        logging.error("ANTHROPIC_API_KEY が設定されていません")
        return None

    today = datetime.now(tz=JST).strftime("%Y-%m-%d")
    prompt = RESEARCH_PROMPT.format(date=today)

    logging.info("KDPトレンドリサーチ開始...")
    try:
        response = _client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        text = next((b.text for b in response.content if b.type == "text"), "")
        code_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        raw = code_match.group(1) if code_match else None
        if not raw:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            raw = match.group() if match else None
        if not raw:
            logging.error("レスポンスにJSONが見つかりません")
            return None
        raw = re.sub(r',\s*([}\]])', r'\1', raw)
        data = json.loads(raw)
        logging.info(f"リサーチ完了: {len(data.get('candidates', []))}件の候補を取得")
        return data
    except json.JSONDecodeError as e:
        logging.error(f"JSONパースエラー: {e}")
        return None
    except Exception as e:
        logging.error(f"リサーチ失敗: {e}")
        return None


def main() -> Optional[dict]:
    setup_file_logging()
    logging.info("=== researcher 開始 ===")

    result = research_topics()
    if result:
        today = datetime.now(tz=JST).strftime("%Y-%m-%d")
        RESEARCH_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_path = RESEARCH_CACHE_DIR / f"{today}.json"
        save_json(cache_path, result)
        logging.info(f"リサーチ結果を保存: {cache_path}")
    else:
        logging.warning("リサーチ失敗")

    logging.info("=== researcher 完了 ===")
    return result


if __name__ == "__main__":
    main()
