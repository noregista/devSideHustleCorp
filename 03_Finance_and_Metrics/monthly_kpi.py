"""
monthly_kpi.py — 月次KPI自動集計

post_history.json と book_history.json を読み込み、
月次KPIレポートを Markdown ファイルとして出力する。

使い方:
  python3 monthly_kpi.py           # 今月のレポートを生成
  python3 monthly_kpi.py 2026-04   # 指定月のレポートを生成
  python3 monthly_kpi.py --all     # 全月分を生成

出力先:
  03_Finance_and_Metrics/KPI_YYYY_MM.md
"""

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent
REPO_DIR = BASE_DIR.parent
THREADS_DIR = REPO_DIR / "01_Threads_Automation"
KDP_DIR = REPO_DIR / "04_KDP_Automation"
POST_HISTORY_PATH = THREADS_DIR / "post_history.json"
BOOK_HISTORY_PATH = KDP_DIR / "book_history.json"

JST = timezone(timedelta(hours=9))


def load_post_history() -> list:
    if not POST_HISTORY_PATH.exists():
        return []
    with open(POST_HISTORY_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_book_history() -> list:
    if not BOOK_HISTORY_PATH.exists():
        return []
    try:
        with open(BOOK_HISTORY_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def get_month_str(dt_str: str) -> str:
    """ISO日付文字列から YYYY-MM を返す。"""
    return dt_str[:7]


def build_threads_stats(posts: list, month: str) -> dict:
    """指定月のThreads投稿統計を集計する。"""
    month_posts = [p for p in posts if p.get("posted_at", "").startswith(month)]

    by_account: dict = defaultdict(lambda: {"count": 0, "genre": ""})
    for p in month_posts:
        acc_id = p.get("account_id", "unknown")
        by_account[acc_id]["count"] += 1
        by_account[acc_id]["genre"] = p.get("genre", "")

    return {
        "total_posts": len(month_posts),
        "by_account": dict(by_account),
    }


def build_kdp_stats(books: list, month: str) -> dict:
    """指定月のKDP統計を集計する。"""
    month_books = [b for b in books if b.get("generated_at", "").startswith(month)]
    published = [b for b in month_books if b.get("status") == "published"]
    pending = [b for b in month_books if b.get("status") == "pending_upload"]
    cancelled = [b for b in month_books if b.get("status") == "cancelled"]

    return {
        "generated": len(month_books),
        "published": len(published),
        "pending": len(pending),
        "cancelled": len(cancelled),
        "books": month_books,
    }


def generate_report(month: str, posts: list, books: list) -> str:
    """月次KPIレポートのMarkdown文字列を生成する。"""
    threads = build_threads_stats(posts, month)
    kdp = build_kdp_stats(books, month)

    year, mon = month.split("-")
    lines = [
        f"# 月次KPI — {year}年{int(mon)}月",
        "",
        f"> 生成日時: {datetime.now(tz=JST).strftime('%Y-%m-%d %H:%M')} JST",
        "",
        "---",
        "",
        "## Threads 投稿実績",
        "",
        f"**総投稿数: {threads['total_posts']}件**",
        "",
        "| アカウント | ジャンル | 投稿数 |",
        "|-----------|---------|--------|",
    ]

    for acc_id, stat in sorted(threads["by_account"].items()):
        lines.append(f"| {acc_id} | {stat['genre']} | {stat['count']}件 |")

    lines += [
        "",
        "---",
        "",
        "## KDP 出版実績",
        "",
        f"| 項目 | 件数 |",
        f"|------|------|",
        f"| 生成冊数 | {kdp['generated']}冊 |",
        f"| 出版済み | {kdp['published']}冊 |",
        f"| アップロード待ち | {kdp['pending']}冊 |",
        f"| キャンセル | {kdp['cancelled']}冊 |",
        "",
    ]

    if kdp["books"]:
        lines += ["### 生成書籍一覧", ""]
        for b in kdp["books"]:
            status_label = {
                "published": "✅ 出版済み",
                "pending_upload": "⏳ アップロード待ち",
                "cancelled": "❌ キャンセル",
            }.get(b.get("status", ""), b.get("status", ""))
            asin = b.get("asin") or "未取得"
            price = b.get("price_jpy") or "-"
            chars = b.get("total_chars", 0)
            lines.append(f"- **{b.get('title', '?')}**")
            lines.append(f"  - ステータス: {status_label}")
            lines.append(f"  - 価格: ¥{price} / ASIN: {asin}")
            lines.append(f"  - 文字数: {chars:,}字")
            lines.append(f"  - 生成日: {b.get('generated_at', '')[:10]}")
            lines.append("")

    lines += [
        "---",
        "",
        "## 収益メモ",
        "",
        "| 項目 | 金額 | 備考 |",
        "|------|------|------|",
        "| Threads 広告収益 | ¥0 | フォロワー数が収益化基準未達 |",
        "| KDP ロイヤリティ | ¥- | 実績は手動で記入 |",
        "| APIコスト（概算） | ¥- | 手動で記入 |",
        "",
        "> ※ 収益・コストの実績は手動で記入してください。",
        "",
        "---",
        "",
        f"*自動生成: monthly_kpi.py | {datetime.now(tz=JST).strftime('%Y-%m-%d')}*",
    ]

    return "\n".join(lines) + "\n"


def get_all_months(posts: list, books: list) -> list[str]:
    """投稿・書籍履歴から全月を列挙する。"""
    months = set()
    for p in posts:
        m = p.get("posted_at", "")[:7]
        if m:
            months.add(m)
    for b in books:
        m = b.get("generated_at", "")[:7]
        if m:
            months.add(m)
    return sorted(months)


def main() -> None:
    args = sys.argv[1:]
    posts = load_post_history()
    books = load_book_history()

    if "--all" in args:
        months = get_all_months(posts, books)
        if not months:
            print("履歴データがありません。")
            return
    elif args and not args[0].startswith("--"):
        months = [args[0]]
    else:
        months = [datetime.now(tz=JST).strftime("%Y-%m")]

    for month in months:
        report = generate_report(month, posts, books)
        output_path = BASE_DIR / f"KPI_{month.replace('-', '_')}.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ {output_path.name} を生成しました")

        # サマリ表示
        threads = build_threads_stats(posts, month)
        kdp = build_kdp_stats(books, month)
        print(f"   Threads投稿: {threads['total_posts']}件 / KDP生成: {kdp['generated']}冊（出版済: {kdp['published']}冊）")


if __name__ == "__main__":
    main()
