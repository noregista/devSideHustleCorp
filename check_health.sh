#!/bin/bash
# check_health.sh — 全プロジェクトの稼働状態チェック
#
# 使い方:
#   bash check_health.sh          # 通常チェック
#   bash check_health.sh --notify # macOS通知あり（Macのみ）
#
# チェック内容:
#   - Threads bot: 最終実行から25時間以上経過していないか
#   - Threads bot: 直近のエラー件数
#   - KDP: 最終実行日時
#   - KDP: 未アップロードのepubがないか

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
THREADS_DIR="$REPO_DIR/01_Threads_Automation"
KDP_DIR="$REPO_DIR/04_KDP_Automation"
NOTIFY=false
[[ "${1:-}" == "--notify" ]] && NOTIFY=true

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

ok()   { echo -e "${GREEN}  ✓ $*${NC}"; }
warn() { echo -e "${YELLOW}  ⚠ $*${NC}"; }
err()  { echo -e "${RED}  ✗ $*${NC}"; }
info() { echo -e "${CYAN}  ▶ $*${NC}"; }

ISSUES=0

send_notification() {
  local title="$1" msg="$2"
  if $NOTIFY && command -v osascript &>/dev/null; then
    osascript -e "display notification \"$msg\" with title \"$title\""
  fi
}

echo ""
echo "=================================================="
echo "  devSideHustleCorp ヘルスチェック"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "=================================================="

# ─────────────────────────────────────────────
# 1. Threads bot チェック
# ─────────────────────────────────────────────
echo ""
echo -e "${CYAN}【01_Threads_Automation】${NC}"

THREADS_LOG="$THREADS_DIR/logs/run_with_pull.log"
if [ ! -f "$THREADS_LOG" ]; then
  err "run_with_pull.log が見つかりません"
  ((ISSUES++))
else
  # 最終実行からの経過時間
  LAST_RUN=$(tail -1 "$THREADS_LOG" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}' | head -1)
  if [ -z "$LAST_RUN" ]; then
    warn "最終実行日時を取得できませんでした"
  else
    NOW_EPOCH=$(date +%s)
    LAST_EPOCH=$(date -j -f "%Y-%m-%d %H:%M:%S" "$LAST_RUN" +%s 2>/dev/null || date -d "$LAST_RUN" +%s 2>/dev/null || echo 0)
    ELAPSED=$(( (NOW_EPOCH - LAST_EPOCH) / 3600 ))

    if [ "$ELAPSED" -ge 25 ]; then
      err "最終実行: $LAST_RUN (${ELAPSED}時間前) — 異常の可能性あり"
      send_notification "Threads Bot 異常" "最終実行から${ELAPSED}時間経過しています"
      ((ISSUES++))
    else
      ok "最終実行: $LAST_RUN (${ELAPSED}時間前)"
    fi
  fi
fi

# エラー件数（直近24時間）
SUPERVISOR_LOG="$THREADS_DIR/logs/supervisor.log"
if [ -f "$SUPERVISOR_LOG" ]; then
  ERROR_COUNT=$(grep -c "\[ERROR\]" "$SUPERVISOR_LOG" 2>/dev/null || true)
  WARN_COUNT=$(grep -c "\[WARNING\]" "$SUPERVISOR_LOG" 2>/dev/null || true)
  ERROR_COUNT=${ERROR_COUNT:-0}
  WARN_COUNT=${WARN_COUNT:-0}
  if [ "$ERROR_COUNT" -gt 0 ]; then
    err "supervisor.log に ERROR ${ERROR_COUNT}件"
    grep "\[ERROR\]" "$SUPERVISOR_LOG" | tail -3 | while read line; do
      echo "      $line"
    done
    ((ISSUES++))
  else
    ok "ERROR 0件 / WARNING ${WARN_COUNT}件"
  fi
fi

# poster.log — 投稿失敗チェック
POSTER_LOG="$THREADS_DIR/logs/poster.log"
if [ -f "$POSTER_LOG" ]; then
  POSTER_ERRORS=$(grep -c "\[ERROR\]\|\[WARNING\]" "$POSTER_LOG" 2>/dev/null || true)
  POSTER_ERRORS=${POSTER_ERRORS:-0}
  LAST_POST=$(grep "投稿完了" "$POSTER_LOG" | tail -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}' | head -1)
  if [ -n "$LAST_POST" ]; then
    ok "最終投稿: $LAST_POST"
  fi
  if [ "$POSTER_ERRORS" -gt 0 ]; then
    warn "poster.log に WARNING/ERROR ${POSTER_ERRORS}件"
  fi
fi

# kill_switch チェック
KILL_SWITCH="$THREADS_DIR/kill_switch.json"
if [ -f "$KILL_SWITCH" ]; then
  IS_KILLED=$(python3 -c "import json; d=json.load(open('$KILL_SWITCH')); print(d.get('active',False))" 2>/dev/null || echo "False")
  if [ "$IS_KILLED" = "True" ]; then
    err "kill_switch が active です！投稿停止中"
    ((ISSUES++))
  else
    ok "kill_switch: 正常（active=false）"
  fi
fi

# ─────────────────────────────────────────────
# 2. KDP チェック
# ─────────────────────────────────────────────
echo ""
echo -e "${CYAN}【04_KDP_Automation】${NC}"

KDP_LOG="$KDP_DIR/logs/main.log"
if [ ! -f "$KDP_LOG" ]; then
  info "main.log なし（未実行）"
else
  LAST_KDP=$(tail -50 "$KDP_LOG" | grep "パイプライン完了\|パイプライン 開始" | tail -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}' | head -1)
  if [ -n "$LAST_KDP" ]; then
    ok "最終KDP実行: $LAST_KDP"
  fi
fi

# book_history.json — pending_upload の件数チェック
BOOK_HISTORY="$KDP_DIR/book_history.json"
if [ -f "$BOOK_HISTORY" ]; then
  PENDING=$(python3 -c "
import json
d = json.load(open('$BOOK_HISTORY'))
pending = [b for b in d if b.get('status') == 'pending_upload']
print(len(pending))
" 2>/dev/null || echo 0)
  if [ "$PENDING" -gt 0 ]; then
    warn "アップロード待ちのepubが ${PENDING}件あります"
    python3 -c "
import json
d = json.load(open('$BOOK_HISTORY'))
for b in d:
    if b.get('status') == 'pending_upload':
        print(f'      - {b[\"title\"]} ({b[\"generated_at\"][:10]})')
" 2>/dev/null || true
  else
    ok "アップロード待ち: 0件"
  fi
fi

# ─────────────────────────────────────────────
# 3. Git 状態チェック
# ─────────────────────────────────────────────
echo ""
echo -e "${CYAN}【Git 状態】${NC}"

UNCOMMITTED=$(git -C "$REPO_DIR" status --short 2>/dev/null | wc -l | tr -d ' ')
if [ "$UNCOMMITTED" -gt 0 ]; then
  warn "未コミットの変更が ${UNCOMMITTED}件あります"
  git -C "$REPO_DIR" status --short 2>/dev/null | head -5 | while read line; do
    echo "      $line"
  done
else
  ok "作業ツリー: クリーン"
fi

# ─────────────────────────────────────────────
# 結果サマリ
# ─────────────────────────────────────────────
echo ""
echo "=================================================="
if [ "$ISSUES" -eq 0 ]; then
  echo -e "${GREEN}  ✓ 全システム正常${NC}"
else
  echo -e "${RED}  ✗ 要確認: ${ISSUES}件の問題があります${NC}"
  send_notification "devSideHustleCorp 要確認" "${ISSUES}件の問題が検出されました"
fi
echo "=================================================="
echo ""
