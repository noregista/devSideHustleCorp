"""
main.py — KDP自動生成パイプライン エントリーポイント

実行フロー:
  STEP 1: researcher.py  → トレンドリサーチ（候補8テーマ生成）
  STEP 2: scorer.py      → スコアリング（最優秀テーマ1件を選定）
  STEP 3: writer.py      → 本文生成（アウトライン → 章ごと執筆）
  STEP 4: formatter.py   → epub変換・表紙生成
  STEP 5: book_history.json に結果を記録

実行方法:
  python3 main.py

cronでの自動実行例（毎週日曜23:00）:
  0 23 * * 0 cd /path/to/04_KDP_Automation && python3 main.py
"""

import json
import logging
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent
LOG_PATH = BASE_DIR / "logs" / "main.log"
BOOK_HISTORY_PATH = BASE_DIR / "book_history.json"
CONFIG_PATH = BASE_DIR / "config.json"
JST = timezone(timedelta(hours=9))

sys.path.insert(0, str(BASE_DIR))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def setup_file_logging() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logging.getLogger().addHandler(handler)


def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    example = BASE_DIR / "config.example.json"
    if example.exists():
        with open(example, encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_history() -> list:
    if not BOOK_HISTORY_PATH.exists():
        return []
    try:
        with open(BOOK_HISTORY_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_history(history: list) -> None:
    tmp = BOOK_HISTORY_PATH.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    tmp.replace(BOOK_HISTORY_PATH)


def set_api_key(config: dict) -> bool:
    key = os.environ.get("ANTHROPIC_API_KEY") or config.get("anthropic_api_key", "")
    if not key or key == "YOUR_ANTHROPIC_API_KEY":
        logging.error("ANTHROPIC_API_KEY が設定されていません。config.json を確認してください。")
        return False
    os.environ["ANTHROPIC_API_KEY"] = key
    return True


def main() -> None:
    setup_file_logging()
    logging.info("=" * 50)
    logging.info("KDP自動生成パイプライン 開始")
    logging.info("=" * 50)

    config = load_config()
    if not set_api_key(config):
        sys.exit(1)

    book_settings = config.get("book_settings", {})
    chapter_count = book_settings.get("chapter_count", 6)

    # --- STEP 1: リサーチ ---
    logging.info("[STEP 1/4] トレンドリサーチ開始")
    from agents.researcher import main as researcher_main
    research_result = researcher_main()
    if not research_result or not research_result.get("candidates"):
        logging.error("リサーチ失敗。終了します。")
        sys.exit(1)
    logging.info(f"  → {len(research_result['candidates'])}件の候補を取得")

    # --- STEP 2: スコアリング ---
    logging.info("[STEP 2/4] テーマスコアリング開始")
    from agents.scorer import main as scorer_main
    score_result = scorer_main(research_result)
    if not score_result:
        logging.error("スコアリング失敗。終了します。")
        sys.exit(1)
    selected = score_result.get("selected_candidate", {})
    kdp_metadata = score_result.get("kdp_metadata", {})
    logging.info(f"  → 選定テーマ: 「{selected.get('title')}」")
    logging.info(f"  → 推奨価格: {kdp_metadata.get('price_jpy')}円")

    # --- STEP 3: 本文生成 ---
    logging.info(f"[STEP 3/4] 本文生成開始（{chapter_count}章構成）")
    from agents.writer import generate_book
    book_data = generate_book(selected, chapter_count=chapter_count)
    if not book_data:
        logging.error("本文生成失敗。終了します。")
        sys.exit(1)
    logging.info(f"  → 合計{book_data['total_chars']:,}字生成完了")

    # --- STEP 4: epub変換 ---
    logging.info("[STEP 4/4] epub変換開始")
    from agents.formatter import build_epub
    output_path = build_epub(book_data, kdp_metadata)
    if not output_path:
        logging.error("epub生成失敗。終了します。")
        sys.exit(1)
    logging.info(f"  → 出力: {output_path}")

    # --- 履歴記録 ---
    history = load_history()
    entry = {
        "generated_at": datetime.now(tz=JST).isoformat(),
        "title": book_data["outline"].get("title", selected.get("title")),
        "author": book_data["outline"].get("author", ""),
        "genre": selected.get("genre", ""),
        "total_chars": book_data["total_chars"],
        "chapter_count": len(book_data["chapters"]),
        "epub_path": str(output_path),
        "kdp_metadata": kdp_metadata,
        "status": "generated",
        "asin": None,
        "published_at": None,
        "price_jpy": kdp_metadata.get("price_jpy"),
    }
    history.append(entry)
    save_history(history)

    logging.info("=" * 50)
    logging.info("✅ パイプライン完了")
    logging.info(f"   タイトル : {entry['title']}")
    logging.info(f"   著者     : {entry['author']}")
    logging.info(f"   文字数   : {entry['total_chars']:,}字")
    logging.info(f"   epub     : {output_path.name}")
    logging.info(f"   推奨価格 : {kdp_metadata.get('price_jpy')}円")
    logging.info("")
    logging.info("【次のステップ】")
    logging.info("  1. output/ フォルダの epub ファイルを確認")
    logging.info("  2. KDPダッシュボード（kdp.amazon.co.jp）にログイン")
    logging.info("  3. 「新しいタイトルを追加」からepubをアップロード")
    logging.info(f"  4. 説明文: {kdp_metadata.get('description', '')[:50]}...")
    logging.info(f"  5. キーワード: {', '.join(kdp_metadata.get('keywords', []))}")
    logging.info("=" * 50)


if __name__ == "__main__":
    main()
