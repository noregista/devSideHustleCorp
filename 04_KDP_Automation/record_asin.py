"""
record_asin.py — KDP出版後にASINとURLをbook_history.jsonに記録する

使い方:
  python3 record_asin.py B0XXXXXXXXX
  python3 record_asin.py B0XXXXXXXXX --title "ChatGPT・Claude完全攻略ガイド"

Claudeからの実行フロー:
  1. pending_upload が1件 → 自動特定してASINを記録
  2. pending_upload が複数件 → 標準出力に候補一覧を出して終了（Claude側でタイトルを確認）
  3. --title 指定あり → タイトルで絞り込んでASINを記録
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
    pending_statuses = ("submitted", "pending_upload", "generated")

    if args.title:
        for entry in reversed(history):
            if args.title in entry.get("title", ""):
                target = entry
                break
    else:
        # pending_upload の件数を確認
        pending_entries = [e for e in history if e.get("status") in pending_statuses]
        if len(pending_entries) == 0:
            print("❌ 記録対象の本が見つかりません")
            sys.exit(1)
        elif len(pending_entries) == 1:
            target = pending_entries[0]
        else:
            # 複数ある場合は一覧を出して終了（Claude側でタイトルを確認するため）
            print("MULTIPLE_PENDING")
            for e in pending_entries:
                print(f"  - {e['title']} [{e.get('status')}] 生成日: {e.get('generated_at', '')[:10]}")
            sys.exit(2)

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

    # Google Tasks の該当タスクを完了にする
    try:
        sys.path.insert(0, str(BASE_DIR.parent / "99_System_Logs"))
        from google_tasks_sync import get_service, get_or_create_tasklist, complete_task
        gt_service = get_service()
        gt_tasklist_id = get_or_create_tasklist(gt_service)
        complete_task(gt_service, gt_tasklist_id, target["title"])
        print(f"   Google Tasks: 完了に更新しました")
    except Exception as e:
        print(f"   Google Tasks: スキップ ({e})")


if __name__ == "__main__":
    main()
