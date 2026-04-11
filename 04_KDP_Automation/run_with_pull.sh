#!/bin/bash
# run_with_pull.sh
# launchd/cron から呼ばれるラッパー。
# 最新コードをpullしてからKDP自動生成パイプラインを実行する。
# ライブラリの自動インストール・config.jsonの自動生成も main.py 内で行われる。

set -euo pipefail

BOT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG="$BOT_DIR/logs/run_with_pull.log"
mkdir -p "$BOT_DIR/logs"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }

log "=== 起動 ==="

# 未コミットの変更があれば stash して保護
STASHED=false
if ! git -C "$BOT_DIR" diff --quiet 2>/dev/null || \
   ! git -C "$BOT_DIR" diff --cached --quiet 2>/dev/null; then
  log "未コミットの変更を検出 → stash して pull 後に復元"
  git -C "$BOT_DIR" stash push -m "auto-stash by run_with_pull $(date '+%Y-%m-%d %H:%M:%S')" 2>>"$LOG"
  STASHED=true
fi

# コード更新
log "git pull 中..."
if git -C "$BOT_DIR" pull --rebase --quiet 2>>"$LOG"; then
  log "git pull 完了"
else
  log "git pull 失敗（ネットワーク不可？）— 既存コードで続行"
fi

# stash を復元
if [ "$STASHED" = true ]; then
  git -C "$BOT_DIR" stash pop 2>>"$LOG" && log "stash 復元完了" || log "stash pop 失敗 — 手動確認してください"
fi

# パイプライン実行（ライブラリインストール・config確認も自動で行われる）
log "main.py 起動"
python3 "$BOT_DIR/main.py"
log "=== 完了 ==="
