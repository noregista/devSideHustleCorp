"""
agents/writer.py

選定されたテーマをもとに電子書籍の本文を生成する。
トークン制限を避けるため「アウトライン生成 → 章ごとに分割生成」の2ステップ方式。

使用モデル: claude-sonnet-4-6（品質重視）
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Optional

try:
    import anthropic as _anthropic_module
    import os
    _client: Optional[Any] = (
        _anthropic_module.Anthropic() if os.environ.get("ANTHROPIC_API_KEY") else None
    )
except ImportError:
    _client = None

TARGET_CHARS_PER_CHAPTER = 2000  # 全体2万字目標（8章構成で約2000字/章）
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

CHAPTER_PROMPT = """
あなたは日本のベストセラー実用書ライターです。
以下の仕様で電子書籍の1章分を執筆してください。

【書籍情報】
タイトル: {book_title}
ターゲット読者: {target_reader}
解決する課題: {core_problem}

【この章の情報】
章番号: {chapter_label}
章タイトル: {chapter_title}
節構成: {sections}
この章で伝えたいこと: {key_message}

【執筆ルール】
- 文字数: {target_chars}字程度
- 読者に語りかける親しみやすい文体（です・ます調）
- 具体的なエピソード・例・数字を積極的に使う
- 各節は見出し（## 節タイトル）で区切る
- 難しい専門用語は使わず、中学生でもわかる言葉で書く
- 読者が「自分のことだ」と感じる共感ポイントを必ず入れる
- 章末に「まとめ」を入れる（箇条書き3〜5点）
- まとめの後に「今すぐできるアクション」を追加する（読者が今日から実践できる具体的な手順を箇条書き3〜5項目）

本文のみ返してください（JSONではなく、そのままのテキスト）。
章タイトルは「# {chapter_title}」の形式で始めること。
"""

SERIES_LINK_TEMPLATE = """

---

## このシリーズの他の作品

{series_items}

同シリーズの最新作は Amazon Kindle でお読みいただけます。
「{author}」で検索してください。
"""


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
        response = _client.messages.create(
            model="claude-sonnet-4-6",
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
            return None
        raw = re.sub(r',\s*([}\]])', r'\1', raw)
        outline = json.loads(raw)
        logging.info(f"アウトライン完成: {len(outline.get('chapters', []))}章構成")
        return outline
    except Exception as e:
        logging.error(f"アウトライン生成失敗: {e}")
        return None


def generate_chapter(
    book_title: str,
    target_reader: str,
    core_problem: str,
    chapter_label: str,
    chapter_title: str,
    sections: list[str],
    key_message: str,
) -> Optional[str]:
    if _client is None:
        return None

    prompt = CHAPTER_PROMPT.format(
        book_title=book_title,
        target_reader=target_reader,
        core_problem=core_problem,
        chapter_label=chapter_label,
        chapter_title=chapter_title,
        sections="、".join(sections),
        key_message=key_message,
        target_chars=TARGET_CHARS_PER_CHAPTER,
    )

    try:
        response = _client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        text = next((b.text for b in response.content if b.type == "text"), "")
        return text.strip()
    except Exception as e:
        logging.error(f"章生成失敗 [{chapter_label}]: {e}")
        return None


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


def generate_book(candidate: dict, chapter_count: int = 6) -> Optional[dict]:
    logging.info("=== writer 開始 ===")

    outline = generate_outline(candidate, chapter_count)
    if not outline:
        logging.error("アウトライン生成失敗")
        return None

    book_title = outline.get("title", candidate.get("title", ""))
    target_reader = candidate.get("target_reader", "")
    core_problem = candidate.get("core_problem", "")
    chapters_content: list[dict] = []

    # はじめに
    intro = outline.get("introduction", {})
    logging.info("「はじめに」生成中...")
    intro_text = generate_chapter(
        book_title=book_title,
        target_reader=target_reader,
        core_problem=core_problem,
        chapter_label="はじめに",
        chapter_title=intro.get("title", "はじめに"),
        sections=intro.get("sections", []),
        key_message=intro.get("key_message", ""),
    )
    if intro_text:
        chapters_content.append({"label": "はじめに", "title": intro.get("title", "はじめに"), "content": intro_text})

    # 本編各章
    for ch in outline.get("chapters", []):
        label = f"第{ch['number']}章"
        logging.info(f"{label}「{ch['title']}」生成中...")
        text = generate_chapter(
            book_title=book_title,
            target_reader=target_reader,
            core_problem=core_problem,
            chapter_label=label,
            chapter_title=ch["title"],
            sections=ch.get("sections", []),
            key_message=ch.get("key_message", ""),
        )
        if text:
            chapters_content.append({"label": label, "title": ch["title"], "content": text})

    # おわりに
    conclusion = outline.get("conclusion", {})
    logging.info("「おわりに」生成中...")
    conclusion_text = generate_chapter(
        book_title=book_title,
        target_reader=target_reader,
        core_problem=core_problem,
        chapter_label="おわりに",
        chapter_title=conclusion.get("title", "おわりに"),
        sections=conclusion.get("sections", []),
        key_message=conclusion.get("key_message", ""),
    )
    if conclusion_text:
        chapters_content.append({"label": "おわりに", "title": conclusion.get("title", "おわりに"), "content": conclusion_text})

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
