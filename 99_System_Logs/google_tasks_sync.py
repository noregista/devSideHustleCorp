"""
google_tasks_sync.py — Business-Tracker.md の未完了タスクを Google Tasks に同期する

初回実行時: ブラウザが開いてGoogleログインが必要（1回のみ）
以降: token.json を使って自動実行

使い方:
  python3 google_tasks_sync.py              # Business-Tracker から同期
  python3 google_tasks_sync.py --clear      # Google Tasks のリストを一旦クリアして同期
  python3 google_tasks_sync.py --list       # 現在のタスク一覧を表示

依存:
  pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
"""

import argparse
import io
import json
import os
import re
import sys
from pathlib import Path

# Windows環境での文字コード対策
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent.parent
TRACKER_PATH = BASE_DIR / "03_Finance_and_Metrics" / "Business-Tracker.md"
CREDENTIALS_PATH = Path(__file__).parent / "google_credentials.json"
TOKEN_PATH = Path(__file__).parent / "google_token.json"
TASK_LIST_NAME = "devSideHustleCorp"

SCOPES = ["https://www.googleapis.com/auth/tasks"]


def get_service():
    """Google Tasks API サービスを取得する（初回はブラウザ認証）"""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        print("❌ 依存パッケージが未インストールです。以下を実行してください:")
        print("   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        sys.exit(1)

    if not CREDENTIALS_PATH.exists():
        print(f"❌ credentials.json が見つかりません: {CREDENTIALS_PATH}")
        print("   Google Cloud Console からダウンロードして配置してください。")
        print("   手順: https://console.cloud.google.com/")
        sys.exit(1)

    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
        print("✅ 認証完了。token.json を保存しました。")

    return build("tasks", "v1", credentials=creds)


def get_or_create_tasklist(service) -> str:
    """devSideHustleCorp タスクリストのIDを取得（なければ作成）"""
    result = service.tasklists().list().execute()
    for tl in result.get("items", []):
        if tl["title"] == TASK_LIST_NAME:
            return tl["id"]
    new_list = service.tasklists().insert(body={"title": TASK_LIST_NAME}).execute()
    print(f"✅ タスクリスト「{TASK_LIST_NAME}」を作成しました")
    return new_list["id"]


def parse_pending_tasks(md_path: Path) -> list[dict]:
    """Business-Tracker.md から未完了タスク（⬜）を抽出する"""
    if not md_path.exists():
        print(f"❌ {md_path} が見つかりません")
        return []

    tasks = []
    content = md_path.read_text(encoding="utf-8")
    current_project = ""

    for line in content.split("\n"):
        # プロジェクト名を取得
        project_match = re.match(r"^### (.+?)（", line)
        if project_match:
            current_project = project_match.group(1).strip()

        # 未完了タスク行を抽出（| ⬜ 未着手 | タスク名 | ... |）
        if "⬜" in line and "|" in line:
            cols = [c.strip() for c in line.split("|") if c.strip()]
            if len(cols) >= 2:
                task_name = cols[1] if len(cols) > 1 else ""
                deadline = cols[2] if len(cols) > 2 else ""
                note = cols[3] if len(cols) > 3 else ""
                if task_name:
                    title = f"[{current_project}] {task_name}" if current_project else task_name
                    notes = f"期限: {deadline}\n備考: {note}".strip() if deadline or note else ""
                    tasks.append({"title": title, "notes": notes})

    return tasks


def sync_tasks(service, tasklist_id: str, tasks: list[dict], clear: bool = False) -> None:
    """Google Tasks にタスクを同期する"""
    if clear:
        existing = service.tasks().list(tasklist=tasklist_id).execute()
        for task in existing.get("items", []):
            service.tasks().delete(tasklist=tasklist_id, task=task["id"]).execute()
        print(f"  🗑️  既存タスクをクリアしました")

    # 既存タイトルを取得（重複防止）
    existing = service.tasks().list(tasklist=tasklist_id).execute()
    existing_titles = {t["title"] for t in existing.get("items", [])}

    added = 0
    for task in tasks:
        if task["title"] in existing_titles:
            continue
        body = {"title": task["title"]}
        if task.get("notes"):
            body["notes"] = task["notes"]
        service.tasks().insert(tasklist=tasklist_id, body=body).execute()
        print(f"  ➕ {task['title']}")
        added += 1

    print(f"\n✅ {added}件のタスクを追加しました（重複 {len(tasks) - added}件はスキップ）")


def list_tasks(service, tasklist_id: str) -> None:
    """現在のタスク一覧を表示する"""
    result = service.tasks().list(tasklist=tasklist_id).execute()
    items = result.get("items", [])
    if not items:
        print("タスクはありません")
        return
    print(f"【{TASK_LIST_NAME}】タスク一覧 ({len(items)}件)")
    for i, task in enumerate(items, 1):
        status = "✅" if task.get("status") == "completed" else "⬜"
        print(f"  {status} {i}. {task['title']}")


def complete_task(service, tasklist_id: str, keyword: str) -> None:
    """キーワードにマッチするタスクを完了にする"""
    result = service.tasks().list(tasklist=tasklist_id, showCompleted=False).execute()
    items = result.get("items", [])
    matched = [t for t in items if keyword in t["title"]]

    if not matched:
        print(f"「{keyword}」にマッチするタスクが見つかりません")
        list_tasks(service, tasklist_id)
        return

    for task in matched:
        service.tasks().patch(
            tasklist=tasklist_id,
            task=task["id"],
            body={"status": "completed"}
        ).execute()
        print(f"  [完了] {task['title']}")

    print(f"\n{len(matched)}件を完了にしました")


def main():
    parser = argparse.ArgumentParser(description="Google Tasks 同期")
    parser.add_argument("--clear", action="store_true", help="既存タスクをクリアして同期")
    parser.add_argument("--list", action="store_true", help="タスク一覧を表示")
    parser.add_argument("--complete", metavar="KEYWORD", help="キーワードにマッチするタスクを完了にする")
    args = parser.parse_args()

    print("Google Tasks に接続中...")
    service = get_service()
    tasklist_id = get_or_create_tasklist(service)

    if args.list:
        list_tasks(service, tasklist_id)
        return

    if args.complete:
        complete_task(service, tasklist_id, args.complete)
        return

    print(f"\nBusiness-Tracker.md から未完了タスクを読み込み中...")
    tasks = parse_pending_tasks(TRACKER_PATH)
    print(f"  → {len(tasks)}件の未完了タスクを検出\n")

    if not tasks:
        print("同期するタスクがありません")
        return

    sync_tasks(service, tasklist_id, tasks, clear=args.clear)


if __name__ == "__main__":
    main()
