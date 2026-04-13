"""
agents/writer.py

選定されたテーマをもとに電子書籍の本文を生成する。
トークン制限を避けるため「アウトライン生成 → 章ごとに分割生成」の2ステップ方式。

最適化:
- Anthropic Batch API: アウトライン確定後、全章を並列バッチ送信（50%コスト削減）
- Prompt Caching: システムプロンプト（書籍情報+全アウトライン+執筆ルール）をキャッシュ化
  → 8章中7章がキャッシュヒット（読み取りコスト 1/10）

使用モデル: claude-sonnet-4-6（品質重視）
"""

from __future__ import annotations

import json
import logging
import re
import time
from pathlib import Path
from typing import Any, Optional

import os

try:
    import anthropic as _anthropic_module
    _client: Optional[Any] = (
        _anthropic_module.Anthropic() if os.environ.get("ANTHROPIC_API_KEY") else None
    )
except ImportError:
    _client = None

try:
    from agents.utils import api_call_with_retry, parse_json_response
except ImportError:
    from utils import api_call_with_retry, parse_json_response  # type: ignore[no-redef]

TARGET_CHARS_PER_CHAPTER = 2000  # 全体2万字目標（8章構成で約2000字/章）

# Batch API ポーリング設定
BATCH_POLL_INTERVAL = 30   # 30秒ごとにポーリング
BATCH_MAX_WAIT = 7200      # 最大2時間待機（通常は数分で完了）

OUTLINE_PROMPT = """
あなたは日本のベストセラー実用書ライターです。
以下のテーマで電子書籍のアウトラインを作成してください。

【テーマ情報】
タイトル: {title}
サブタイトル: {subtitle}
ターゲット読者: {target_reader}
解決する課題: {core_problem}
差別化ポイント: {key_selling_point}

【アウトライン要件】
- はじめに（序章）: 1章
- 本編: {chapter_count}章
- おわりに（結論）: 1章
- 各章に3〜5節を含む
- 読者が「これ読みたい」と思える章タイトルにする

以下のJSON形式のみで返してください：

{{
  "title": "最終タイトル",
  "subtitle": "最終サブタイトル",
  "author": "著者名（ペンネーム、日本人らしい名前）",
  "introduction": {{
    "title": "はじめに",
    "sections": ["節タイトル1", "節タイトル2", "節タイトル3"],
    "key_message": "この章で伝えたいこと"
  }},
  "chapters": [
    {{
      "number": 1,
      "title": "章タイトル",
      "sections": ["節タイトル1", "節タイトル2", "節タイトル3", "節タイトル4"],
      "key_message": "この章で伝えたいこと"
    }}
  ],
  "conclusion": {{
    "title": "おわりに",
    "sections": ["節タイトル1", "節タイトル2"],
    "key_message": "この章で伝えたいこと"
  }}
}}
"""

SERIES_LINK_TEMPLATE = """

---

## このシリーズの他の作品

{series_items}

同シリーズの最新作は Amazon Kindle でお読みいただけます。
「{author}」で検索してください。
"""


AUDIT_PROMPT = """
以下の章本文を読んで、品質基準を満たしているか確認してください。

【チェック項目】
1. 具体的な数値・事例が1つ以上含まれているか
2. 「今すぐできるアクション」セクションが存在するか
3. 章末に「まとめ」が含まれているか
4. 専門性・根拠を示す表現（「〜の調査では」等）があるか

以下のJSONのみで返してください：
{{"pass": true, "issues": []}}

---
{chapter_text}
"""


# ---------------------------------------------------------------------------
# プロンプト構築（キャッシュ対象のシステムプロンプト）
# ---------------------------------------------------------------------------

def _build_system_prompt(
    book_title: str,
    target_reader: str,
    core_problem: str,
    outline: dict,
) -> str:
    """
    章生成用システムプロンプトを構築する。
    全章で共通の内容（書籍情報 + 全アウトライン + 執筆ルール）を含み、
    Prompt Caching の対象（1024トークン以上）になるよう設計。
    """
    chapters_summary = json.dumps(
        {
            "introduction": outline.get("introduction", {}),
            "chapters": outline.get("chapters", []),
            "conclusion": outline.get("conclusion", {}),
        },
        ensure_ascii=False,
        indent=2,
    )
    return f"""あなたは日本のベストセラー実用書ライターです。
これから執筆する書籍の全体像と執筆ルールを以下に示します。各章の執筆指示はユーザーメッセージで送ります。

【書籍情報】
タイトル: {book_title}
ターゲット読者: {target_reader}
解決する課題: {core_problem}

【書籍アウトライン（全体構成）】
{chapters_summary}

【執筆ルール（全章共通）】
- 文字数: {TARGET_CHARS_PER_CHAPTER}字程度
- 読者に語りかける親しみやすい文体（です・ます調）
- 具体的なエピソード・例・数字を積極的に使う
- 各節は見出し（## 節タイトル）で区切る
- 難しい専門用語は使わず、中学生でもわかる言葉で書く
- 読者が「自分のことだ」と感じる共感ポイントを必ず入れる
- 章末に「まとめ」を入れる（箇条書き3〜5点）
- まとめの後に「今すぐできるアクション」を追加する（読者が今日から実践できる具体的な手順を箇条書き3〜5項目）
- 章の冒頭は「# 章タイトル」の形式で始めること
- 段落は3〜5文を目安にする（一文は60字以内）
- 具体例は「たとえば〜」「実際に〜」「ある〜の場合〜」のような導入を使う
- 各節の終わりに「つまり〜」「要するに〜」でまとめを入れると読者が理解しやすい

【E-A-T品質基準（必須）】

専門性（Expertise）:
- 各節に具体的な数値・事例・手順を1つ以上必ず含める
- 抽象的な説明だけで終わらず、「具体的に何をするか」を明示する
- 読者が「実際にできる」と感じる粒度で書く

権威性（Authoritativeness）:
- 「〜という研究では」「〜の調査によると」「〜の統計では」など根拠を示す表現を積極的に使う
- 信頼できる情報源（厚生労働省、総務省、主要企業の調査など）への言及を含める
- 専門家の知見や実績のある手法を引用する

信頼性（Trustworthiness）:
- 「うまくいかないケース」や「注意点」「よくある失敗」も正直に書く
- 過剰な約束をせず、現実的な期待値を設定する
- 「〜の場合は効果が限定的です」など、適切な留保を入れる

本文のみ返してください（JSONではなく、そのままのテキスト）。"""


def _build_chapter_user_prompt(
    chapter_label: str,
    chapter_title: str,
    sections: list[str],
    key_message: str,
) -> str:
    """章固有のユーザープロンプト（短い・非キャッシュ）"""
    return f"""以下の章を執筆してください：

章番号: {chapter_label}
章タイトル: {chapter_title}
節構成: {' 、'.join(sections)}
この章で伝えたいこと: {key_message}"""


# ---------------------------------------------------------------------------
# 品質監査
# ---------------------------------------------------------------------------

def audit_chapter(chapter_text: str) -> bool:
    """Haiku で章の品質を自動監査する。pass=False の場合は警告ログを出す。"""
    if _client is None:
        return True  # クライアント未設定時はスキップ
    prompt = AUDIT_PROMPT.format(chapter_text=chapter_text[:3000])  # 先頭3000字で判定
    try:
        response = api_call_with_retry(
            _client.messages.create,
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        text = next((b.text for b in response.content if b.type == "text"), "")
        result = parse_json_response(text)
        if result and not result.get("pass", True):
            issues = result.get("issues", [])
            logging.warning(f"品質監査: 改善点あり → {issues}")
            return False
        return True
    except Exception as e:
        logging.warning(f"品質監査スキップ（エラー）: {e}")
        return True


# ---------------------------------------------------------------------------
# アウトライン生成
# ---------------------------------------------------------------------------

def generate_outline(candidate: dict, chapter_count: int = 6) -> Optional[dict]:
    if _client is None:
        return None

    prompt = OUTLINE_PROMPT.format(
        title=candidate.get("title", ""),
        subtitle=candidate.get("subtitle", ""),
        target_reader=candidate.get("target_reader", ""),
        core_problem=candidate.get("core_problem", ""),
        key_selling_point=candidate.get("key_selling_point", ""),
        chapter_count=chapter_count,
    )

    logging.info("アウトライン生成中...")
    try:
        response = api_call_with_retry(
            _client.messages.create,
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        text = next((b.text for b in response.content if b.type == "text"), "")
        outline = parse_json_response(text)
        if outline:
            logging.info(f"アウトライン完成: {len(outline.get('chapters', []))}章構成")
        return outline
    except Exception as e:
        logging.error(f"アウトライン生成失敗: {e}")
        return None


# ---------------------------------------------------------------------------
# Batch API による全章一括生成（メインフロー）
# ---------------------------------------------------------------------------

def generate_chapters_batch(
    book_title: str,
    target_reader: str,
    core_problem: str,
    outline: dict,
    chapter_specs: list[dict],
) -> dict[str, Optional[str]]:
    """
    Anthropic Batch API で全章を一括生成する（50%コスト削減）。
    システムプロンプトに cache_control を付与し、2章目以降はキャッシュヒット。

    chapter_specs: [{"custom_id": str, "label": str, "title": str,
                     "sections": list, "key_message": str}]
    戻り値: {custom_id: chapter_text or None}
    """
    if _client is None:
        return {}

    system_prompt_text = _build_system_prompt(book_title, target_reader, core_problem, outline)

    # システムプロンプトはキャッシュ対象（ephemeral）
    system_block = [
        {
            "type": "text",
            "text": system_prompt_text,
            "cache_control": {"type": "ephemeral"},
        }
    ]

    requests = []
    for spec in chapter_specs:
        user_content = _build_chapter_user_prompt(
            spec["label"], spec["title"], spec["sections"], spec["key_message"]
        )
        requests.append({
            "custom_id": spec["custom_id"],
            "params": {
                "model": "claude-sonnet-4-6",
                "max_tokens": 4096,
                "system": system_block,
                "messages": [{"role": "user", "content": user_content}],
            },
        })

    logging.info(f"Batch API 送信: {len(requests)}章を一括生成（prompt_caching 有効）...")
    try:
        batch = _client.messages.batches.create(requests=requests)
        batch_id = batch.id
        logging.info(f"Batch送信完了: ID={batch_id}")
    except Exception as e:
        logging.error(f"Batch送信失敗: {e}")
        return {}

    # ポーリング（処理完了まで待機）
    waited = 0
    while waited < BATCH_MAX_WAIT:
        time.sleep(BATCH_POLL_INTERVAL)
        waited += BATCH_POLL_INTERVAL
        try:
            batch = _client.messages.batches.retrieve(batch_id)
            counts = batch.request_counts
            logging.info(
                f"Batch状態: {batch.processing_status} "
                f"({waited}s経過) 完了:{counts.succeeded} "
                f"処理中:{counts.processing} エラー:{counts.errored}"
            )
            if batch.processing_status == "ended":
                break
        except Exception as e:
            logging.warning(f"Batchポーリングエラー: {e}")

    if batch.processing_status != "ended":
        logging.error(f"Batchタイムアウト: {BATCH_MAX_WAIT}秒を超えました")
        return {}

    # 結果収集
    results: dict[str, Optional[str]] = {}
    try:
        for result in _client.messages.batches.results(batch_id):
            cid = result.custom_id
            if result.result.type == "succeeded":
                text = next(
                    (b.text for b in result.result.message.content if b.type == "text"),
                    None,
                )
                results[cid] = text.strip() if text else None
            else:
                logging.warning(f"Batch章生成失敗 [{cid}]: {result.result.type}")
                results[cid] = None
    except Exception as e:
        logging.error(f"Batch結果取得失敗: {e}")

    succeeded = sum(1 for v in results.values() if v)
    logging.info(f"Batch完了: {succeeded}/{len(requests)}章 生成成功")
    return results


# ---------------------------------------------------------------------------
# 単章生成（Batch失敗時のフォールバック）
# ---------------------------------------------------------------------------

def generate_chapter(
    book_title: str,
    target_reader: str,
    core_problem: str,
    chapter_label: str,
    chapter_title: str,
    sections: list[str],
    key_message: str,
    system_prompt_text: Optional[str] = None,
) -> Optional[str]:
    """
    1章分を単独生成する（Batch API失敗時のフォールバック）。
    system_prompt_text が渡された場合はキャッシュ対象のシステムプロンプトを使用。
    """
    if _client is None:
        return None

    user_content = _build_chapter_user_prompt(
        chapter_label, chapter_title, sections, key_message
    )

    try:
        if system_prompt_text:
            # キャッシュ有効: システムプロンプト + 短いユーザープロンプト
            response = api_call_with_retry(
                _client.messages.create,
                model="claude-sonnet-4-6",
                max_tokens=4096,
                system=[
                    {
                        "type": "text",
                        "text": system_prompt_text,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                messages=[{"role": "user", "content": user_content}],
            )
        else:
            # フォールバック: 従来の単一プロンプト方式
            legacy_prompt = f"""あなたは日本のベストセラー実用書ライターです。
書籍「{book_title}」の{chapter_label}「{chapter_title}」を執筆してください。
節構成: {'、'.join(sections)}
伝えたいこと: {key_message}
文字数: {TARGET_CHARS_PER_CHAPTER}字程度。章末に「まとめ」と「今すぐできるアクション」を追加。
本文のみ返してください。章タイトルは「# {chapter_title}」で始めること。"""
            response = api_call_with_retry(
                _client.messages.create,
                model="claude-sonnet-4-6",
                max_tokens=4096,
                messages=[{"role": "user", "content": legacy_prompt}],
            )

        text = next((b.text for b in response.content if b.type == "text"), "")
        chapter_text = text.strip()
        audit_chapter(chapter_text)
        return chapter_text
    except Exception as e:
        logging.error(f"章生成失敗 [{chapter_label}]: {e}")
        return None


# ---------------------------------------------------------------------------
# 巻末シリーズリンク
# ---------------------------------------------------------------------------

def _build_series_link_section(current_title: str, author: str) -> str:
    """book_history.jsonから既刊（published/submitted）を読み込み巻末リンクセクションを生成する"""
    history_path = Path(__file__).parent.parent / "book_history.json"
    if not history_path.exists():
        return ""

    try:
        with open(history_path, encoding="utf-8") as f:
            history: list[dict] = json.load(f)
    except Exception:
        return ""

    items = []
    for entry in history:
        if entry.get("status") not in ("published", "submitted"):
            continue
        title = entry.get("title", "")
        if title == current_title:
            continue
        asin = entry.get("asin")
        if asin:
            url = f"https://www.amazon.co.jp/dp/{asin}"
            items.append(f"- **{title}** → {url}")
        else:
            items.append(f"- **{title}**（Amazon Kindle にて販売中）")

    if not items:
        return ""

    return SERIES_LINK_TEMPLATE.format(
        series_items="\n".join(items),
        author=author,
    )


# ---------------------------------------------------------------------------
# メインオーケストレーション
# ---------------------------------------------------------------------------

def generate_book(candidate: dict, chapter_count: int = 6) -> Optional[dict]:
    logging.info("=== writer 開始 ===")

    outline = generate_outline(candidate, chapter_count)
    if not outline:
        logging.error("アウトライン生成失敗")
        return None

    book_title = outline.get("title", candidate.get("title", ""))
    target_reader = candidate.get("target_reader", "")
    core_problem = candidate.get("core_problem", "")

    # 全章のスペックをリスト化（順番を保持）
    intro = outline.get("introduction", {})
    conclusion = outline.get("conclusion", {})

    chapter_specs: list[dict] = []
    chapter_specs.append({
        "custom_id": "intro",
        "label": "はじめに",
        "title": intro.get("title", "はじめに"),
        "sections": intro.get("sections", []),
        "key_message": intro.get("key_message", ""),
    })
    for ch in outline.get("chapters", []):
        chapter_specs.append({
            "custom_id": f"ch_{ch['number']}",
            "label": f"第{ch['number']}章",
            "title": ch["title"],
            "sections": ch.get("sections", []),
            "key_message": ch.get("key_message", ""),
        })
    chapter_specs.append({
        "custom_id": "conclusion",
        "label": "おわりに",
        "title": conclusion.get("title", "おわりに"),
        "sections": conclusion.get("sections", []),
        "key_message": conclusion.get("key_message", ""),
    })

    total_chapters = len(chapter_specs)
    logging.info(f"Batch API で {total_chapters}章を一括送信中...")

    # ── メインフロー: Batch API（50%コスト削減 + Prompt Caching）──
    batch_results = generate_chapters_batch(
        book_title=book_title,
        target_reader=target_reader,
        core_problem=core_problem,
        outline=outline,
        chapter_specs=chapter_specs,
    )

    # ── フォールバック: Batch失敗時はシーケンシャル生成 ──
    if not batch_results:
        logging.warning("Batch API失敗 → シーケンシャル生成にフォールバック（Prompt Caching継続）")
        system_prompt_text = _build_system_prompt(book_title, target_reader, core_problem, outline)
        batch_results = {}
        for spec in chapter_specs:
            logging.info(f"{spec['label']}「{spec['title']}」生成中...")
            text = generate_chapter(
                book_title=book_title,
                target_reader=target_reader,
                core_problem=core_problem,
                chapter_label=spec["label"],
                chapter_title=spec["title"],
                sections=spec["sections"],
                key_message=spec["key_message"],
                system_prompt_text=system_prompt_text,
            )
            if text:
                batch_results[spec["custom_id"]] = text

    # 順番通りに整列 + 品質監査
    chapters_content: list[dict] = []
    for spec in chapter_specs:
        text = batch_results.get(spec["custom_id"])
        if text:
            audit_chapter(text)
            chapters_content.append({
                "label": spec["label"],
                "title": spec["title"],
                "content": text,
            })

    total_chars = sum(len(c["content"]) for c in chapters_content)
    logging.info(f"本文生成完了: {len(chapters_content)}章 / 合計{total_chars:,}字")

    # 巻末シリーズリンク
    author = outline.get("author", "")
    series_section = _build_series_link_section(book_title, author)
    if series_section:
        logging.info("巻末シリーズリンクを追加")

    logging.info("=== writer 完了 ===")

    return {
        "outline": outline,
        "chapters": chapters_content,
        "total_chars": total_chars,
        "series_section": series_section,
    }


if __name__ == "__main__":
    sample_candidate = {
        "title": "サンプル本",
        "subtitle": "サブタイトル",
        "target_reader": "30代会社員",
        "core_problem": "仕事の効率が上がらない",
        "key_selling_point": "具体的な手順が書いてある",
    }
    result = generate_book(sample_candidate, chapter_count=3)
    if result:
        print(f"生成完了: {result['total_chars']:,}字")
