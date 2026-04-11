"""
record_asin.py — KDP出版後にASINとURLをbook_history.jsonに記録する

使い方:
  python3 record_asin.py B0XXXXXXXXX
  python3 record_asin.py B0XXXXXXXXX --title "ChatGPT・Claude完全攻略ガイド"
"""

import json
import sys
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent
BOOK_HISTORY_PATH = BASE_DIR / "book_history.json"
JST = timezone(timedelta(hours=9))


def load_history() -> list:
    if not BOOK_HISTORY_PATH.exists():
        return []
    with open(BOOK_HISTORY_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_history(history: list) -> None:
    tmp = BOOK_HISTORY_PATH.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    tmp.replace(BOOK_HISTORY_PATH)


def main():
    parser = argparse.ArgumentParser(description="KDP出版後のASIN記録")
    parser.add_argument("asin", help="KDPのASIN（例: B0XXXXXXXXX）")
    parser.add_argument("--title", help="タイトルで対象を絞り込む（省略時は最新の未出版本）")
    args = parser.parse_args()

    history = load_history()
    if not history:
        print("❌ book_history.json が見つかりません")
        sys.exit(1)

    # 対象を選定
    target = None
    if args.title:
        for entry in reversed(history):
            if args.title in entry.get("title", ""):
                target = entry
                break
    else:
        # 最新の未出版本（submitted / pending_upload / generated）
        for entry in reversed(history):
            if entry.get("status") in ("submitted", "pending_upload", "generated"):
                target = entry
                break

    if not target:
        print("❌ 記録対象の本が見つかりません")
        print("   現在のステータス:")
        for e in history:
            print(f"   - {e['title']} [{e.get('status')}]")
        sys.exit(1)

    # 更新
    asin = args.asin.strip()
    target["asin"] = asin
    target["status"] = "published"
    target["published_at"] = datetime.now(tz=JST).isoformat()
    target["amazon_url"] = f"https://www.amazon.co.jp/dp/{asin}"

    save_history(history)

    print(f"✅ ASIN記録完了")
    print(f"   タイトル  : {target['title']}")
    print(f"   ASIN      : {asin}")
    print(f"   URL       : {target['amazon_url']}")
    print(f"   出版日時  : {target['published_at']}")


if __name__ == "__main__":
    main()
