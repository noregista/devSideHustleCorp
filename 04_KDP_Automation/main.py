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
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent
LOG_PATH = BASE_DIR / "logs" / "main.log"
BOOK_HISTORY_PATH = BASE_DIR / "book_history.json"
CONFIG_PATH = BASE_DIR / "config.json"
CONFIG_EXAMPLE_PATH = BASE_DIR / "config.example.json"
REQUIREMENTS_PATH = BASE_DIR / "requirements.txt"
KDP_PAUSE_PATH = BASE_DIR / "kdp_pause.json"
JST = timezone(timedelta(hours=9))


def ensure_requirements() -> None:
    """requirements.txt のライブラリが未インストールなら自動インストールする。"""
    if not REQUIREMENTS_PATH.exists():
        return
    try:
        import ebooklib  # noqa: F401
        from PIL import Image  # noqa: F401
    except ImportError:
        logging.info("依存ライブラリが不足しています。自動インストールします...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_PATH), "-q"]
        )
        logging.info("インストール完了")


def ensure_config() -> bool:
    """config.json が存在しなければ example からコピーして警告を出す。"""
    if CONFIG_PATH.exists():
        return True
    if CONFIG_EXAMPLE_PATH.exists():
        import shutil
        shutil.copy(CONFIG_EXAMPLE_PATH, CONFIG_PATH)
        logging.warning("=" * 50)
        logging.warning("config.json を自動生成しました。")
        logging.warning(f"  {CONFIG_PATH}")
        logging.warning("ANTHROPIC_API_KEY を記入してから再実行してください。")
        logging.warning("=" * 50)
        return False
    logging.error("config.example.json が見つかりません")
    return False

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
    # Gemini フォールバック用キーをセット（config.json から読み込み）
    gemini_key = os.environ.get("GEMINI_API_KEY") or config.get("gemini_api_key", "")
    if gemini_key:
        os.environ["GEMINI_API_KEY"] = gemini_key
        logging.info("GEMINI_API_KEY セット済み（Overload時フォールバック有効）")
    return True


def generate_kdp_upload_info(entry: dict, output_dir: Path) -> None:
    """KDP登録に必要な全情報をMarkdownファイルに出力する"""
    title = entry["title"]
    author = entry["author"]
    meta = entry["kdp_metadata"]
    price = meta.get("price_jpy", 980)
    description = meta.get("description", "")
    keywords = meta.get("keywords", [])

    kw_lines = "\n".join(f"{i+1}. {kw}" for i, kw in enumerate(keywords))

    content = f"""# KDP アップロード情報 — {title}

生成日時: {entry['generated_at']}

---

## Step 1: Kindle本の詳細

| 項目 | 入力値 |
|------|--------|
| 言語 | 日本語 |
| 本のタイトル | {title} |
| サブタイトル | （空欄） |
| シリーズ・レーベル・版 | （全て空欄） |
| 著者氏名 | {author} |
| 権利 | 私は著作権者であり〜を選択 |
| 露骨な性的表現 | いいえ |
| 対象年齢 | 空欄 |
| 主なマーケットプレイス | Amazon.co.jp |

### 内容紹介（コピーして貼り付け）

{description}

### カテゴリー
1. ビジネス・経済 → 業務改善
2. コンピュータ・IT → 一般・入門書 → その他の入門書

### キーワード（7つ、1つずつ入力）

{kw_lines}

### 本の発売オプション
`本の発売準備ができました` を選択

---

## Step 2: Kindle本のコンテンツ

| 項目 | 設定値 |
|------|--------|
| ページを読む方向 | 左から右（横書き） |
| DRM | はい（適用する） |
| 原稿 | output/ の .epub ファイル |
| 表紙 | output/ の .jpg ファイル（fal.ai生成） |
| AI生成コンテンツ | はい |
| ISBN・出版社・主コード | 全て空欄 |
| アクセシビリティ | スキップ |

---

## Step 3: 価格設定

| 項目 | 設定値 |
|------|--------|
| KDPセレクト | 登録しない |
| 出版地域 | すべての地域（全世界） |
| ロイヤリティ | 70% |
| Amazon.co.jp価格 | ¥{price} |

→ 他マーケットプレイスの価格は自動計算される

---

## epub転送（Macで実行）

```bash
cd ~/dev/devSideHustleCorp/04_KDP_Automation
bash transfer_to_windows.sh
```

---

## 出版後: ASIN記録（Macで実行）

```bash
cd ~/dev/devSideHustleCorp/04_KDP_Automation
python3 record_asin.py B0XXXXXXXXX
```
"""

    info_path = output_dir / "KDP_upload_info.md"
    with open(info_path, "w", encoding="utf-8") as f:
        f.write(content)
    logging.info(f"KDPアップロード情報生成: {info_path}")


def main() -> None:
    setup_file_logging()
    _pipeline_start = datetime.now(tz=JST)  # パイプライン開始時刻（generation_minutes算出用）

    # 一時停止チェック（kdp_pause.json: {"active": true} で停止）
    if KDP_PAUSE_PATH.exists():
        try:
            with open(KDP_PAUSE_PATH, encoding="utf-8") as f:
                pause = json.load(f)
            if pause.get("active", False):
                logging.info("KDP一時停止中（kdp_pause.json: active=true）。スキップします。")
                sys.exit(0)
        except Exception:
            pass

    config = load_config()
    dry_run = config.get("dry_run", False)

    logging.info("=" * 50)
    if dry_run:
        logging.info("KDP自動生成パイプライン 開始 [DRY RUN モード]")
        logging.info("  → API呼び出しは実行するが、ファイル保存・外部投稿はスキップ")
    else:
        logging.info("KDP自動生成パイプライン 開始")
    logging.info("=" * 50)

    ensure_requirements()
    if not ensure_config():
        sys.exit(1)

    if not set_api_key(config):
        sys.exit(1)

    book_settings = config.get("book_settings", {})
    chapter_count = book_settings.get("chapter_count", 6)

    # --- STEP 1: リサーチ ---
    logging.info("[STEP 1/4] トレンドリサーチ開始")
    from agents.researcher import main as researcher_main

    # 当日のキャッシュが存在する場合は再利用（APIコスト節約）
    today = datetime.now(tz=JST).strftime("%Y-%m-%d")
    cache_path = BASE_DIR / "research_cache" / f"{today}.json"
    if cache_path.exists():
        logging.info(f"  → 本日のリサーチキャッシュを再利用: {cache_path.name}")
        with open(cache_path, encoding="utf-8") as f:
            research_result = json.load(f)
    else:
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
    fal_key = config.get("fal_key", "")
    output_path = build_epub(book_data, kdp_metadata, fal_key=fal_key)
    if not output_path:
        logging.error("epub生成失敗。終了します。")
        sys.exit(1)
    logging.info(f"  → 出力: {output_path}")

    # --- 履歴・外部連携（dry_run 時はスキップ）---
    entry = {
        "generated_at": datetime.now(tz=JST).isoformat(),
        "title": book_data["outline"].get("title", selected.get("title")),
        "author": book_data["outline"].get("author", ""),
        "genre": selected.get("genre", ""),
        "total_chars": book_data["total_chars"],
        "chapter_count": len(book_data["chapters"]),
        "epub_path": str(output_path),
        "kdp_metadata": kdp_metadata,
        "status": "pending_upload",
        "asin": None,
        "published_at": None,
        "price_jpy": kdp_metadata.get("price_jpy"),
    }

    if dry_run:
        logging.info("[DRY RUN] book_history.json への書き込みをスキップ")
        logging.info("[DRY RUN] KDP_upload_info.md の生成をスキップ")
        logging.info("[DRY RUN] Google Tasks への追加をスキップ")
    else:
        # 履歴記録
        history = load_history()
        history.append(entry)
        save_history(history)

        # KDPアップロード情報生成
        generate_kdp_upload_info(entry, output_path.parent)

        # Google Tasks にアップロードTODOを追加
        try:
            sys.path.insert(0, str(BASE_DIR.parent / "99_System_Logs"))
            from google_tasks_sync import get_service, get_or_create_tasklist, sync_tasks
            gt_service = get_service()
            gt_tasklist_id = get_or_create_tasklist(gt_service)
            gt_task = {
                "title": f"[KDP] アップロード「{entry['title']}」",
                "notes": f"epub: {output_path.name}\n推奨価格: ¥{kdp_metadata.get('price_jpy', 980)}",
            }
            sync_tasks(gt_service, gt_tasklist_id, [gt_task])
            logging.info("Google Tasks にアップロードTODOを追加しました")
        except Exception as e:
            logging.warning(f"Google Tasks追加スキップ: {e}")

    # --- Threads告知投稿（dry_run=True なら投稿せずログのみ）---
    from agents.threads_notifier import notify as threads_notify
    generation_minutes = max(1, int((datetime.now(tz=JST) - _pipeline_start).total_seconds() / 60))
    threads_notify(entry, config, generation_minutes=generation_minutes, dry_run=dry_run)

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
