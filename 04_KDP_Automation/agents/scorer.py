"""
agents/scorer.py

researcher.pyが生成した候補テーマをスコアリングし、
最も売れやすい1テーマを選定する。

使用モデル: claude-haiku-4-5（コスト最小化）
"""

from __future__ import annotations

import json
import logging
import re
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
    from agents.utils import call_claude, parse_json_response
except ImportError:
    from utils import call_claude, parse_json_response  # type: ignore[no-redef]

SCORE_PROMPT = """
あなたはAmazon KDP日本語市場の専門家です。
以下の電子書籍候補テーマを評価し、最も売れる可能性が高い1つを選定してください。

【候補テーマ一覧】
{candidates_json}

【評価基準（各10点満点）】
1. 市場需要: 日本語KDP市場での需要の大きさ
2. 競合の少なさ: 既存書籍が少なく差別化しやすいか
3. 収益ポテンシャル: 単価設定・売れ続ける期間
4. 執筆可能性: AIが高品質なコンテンツを生成できるか
5. タイムリー性: 今この時期に出す意義があるか
6. AIプレミアム需要: AI活用・副業・自動化系テーマは2026年市場で+10万円/月の単価プレミアムが確認されており、関連テーマは需要が特に高い

以下のJSON形式のみで返してください：

{{
  "selected_index": 選択した候補のインデックス番号（0始まり）,
  "scores": [
    {{
      "index": 0,
      "market_demand": 点数,
      "low_competition": 点数,
      "revenue_potential": 点数,
      "writability": 点数,
      "timeliness": 点数,
      "ai_premium_demand": 点数,
      "total": 合計点数,
      "reason": "この点数をつけた理由（1行）"
    }}
  ],
  "selection_reason": "この候補を選んだ理由（2〜3行）",
  "kdp_metadata": {{
    "price_jpy": 推奨価格（円、250〜1200の範囲）,
    "categories": ["KDPカテゴリ1", "KDPカテゴリ2"],
    "keywords": ["キーワード1", "キーワード2", "キーワード3", "キーワード4", "キーワード5", "キーワード6", "キーワード7"],
    "description": "KDP商品説明文（150字程度、購買意欲を高める文章）"
  }}
}}
"""


def score_candidates(candidates: list[dict], gemini_key: str = "") -> Optional[dict]:
    if _client is None:
        logging.error("ANTHROPIC_API_KEY が設定されていません")
        return None
    if not candidates:
        logging.error("候補リストが空です")
        return None

    candidates_json = json.dumps(
        [{"index": i, **c} for i, c in enumerate(candidates)],
        ensure_ascii=False, indent=2
    )
    prompt = SCORE_PROMPT.format(candidates_json=candidates_json)

    logging.info(f"スコアリング開始: {len(candidates)}件の候補を評価中...")
    try:
        text = call_claude(
            _client, prompt,
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            gemini_key=gemini_key,
        )
        if not text:
            return None
        result = parse_json_response(text)
        if not result:
            return None

        selected_idx = result.get("selected_index", 0)
        selected = candidates[selected_idx]
        result["selected_candidate"] = selected
        logging.info(f"選定完了: 「{selected.get('title')}」（index={selected_idx}）")
        return result
    except Exception as e:
        logging.error(f"スコアリング失敗: {e}")
        return None


def main(research_result: dict) -> Optional[dict]:
    logging.info("=== scorer 開始 ===")
    candidates = research_result.get("candidates", [])
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    result = score_candidates(candidates, gemini_key=gemini_key)
    logging.info("=== scorer 完了 ===")
    return result


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sample_path = Path(__file__).parent.parent / "research_cache"
    files = sorted(sample_path.glob("*.json"))
    if files:
        data = json.loads(files[-1].read_text(encoding="utf-8"))
        result = main(data)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("research_cacheにファイルがありません。先にresearcher.pyを実行してください。")
