#!/bin/bash
# =============================================================
# transfer_to_windows.sh — epub等をGit経由でWindowsへ転送する
# 使い方: bash transfer_to_windows.sh
# =============================================================
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✓ $*${NC}"; }
info() { echo -e "${YELLOW}▶ $*${NC}"; }
err()  { echo -e "${RED}✗ $*${NC}"; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 未出版（pending_upload / generated）の最新タイトルを取得
TITLE=$(python3 -c "
import json, sys
try:
    h = json.load(open('book_history.json'))
    pending = [b for b in h if b.get('status') in ('generated', 'pending_upload')]
    print(pending[-1]['title'] if pending else '新刊')
except Exception:
    print('新刊')
" 2>/dev/null || echo "新刊")

info "転送対象: $TITLE"
echo ""

# output/ に転送対象ファイルがあるか確認
ADDED=0
FILES_TO_ADD=()

for f in output/*.epub; do
    [ -f "$f" ] && FILES_TO_ADD+=("$f") && ADDED=$((ADDED + 1))
done
for f in output/*.jpg; do
    [ -f "$f" ] && FILES_TO_ADD+=("$f") && ADDED=$((ADDED + 1))
done
[ -f "output/KDP_upload_info.md" ] && FILES_TO_ADD+=("output/KDP_upload_info.md") && ADDED=$((ADDED + 1))

if [ $ADDED -eq 0 ]; then
    err "output/ に転送するファイルがありません。main.py を先に実行してください。"
fi

# git add -f で .gitignore に関係なく強制追加（.gitignore は変更しない）
for f in "${FILES_TO_ADD[@]}"; do
    git add -f "$f"
    info "  追加: $f"
done

git commit -m "[KDP] epub一時転送: $TITLE

- Windows側でKDPアップロード後に git rm で削除すること
背景: Mac生成epubをWindows環境のKDPダッシュボードから投稿するため"

git push

echo ""
ok "プッシュ完了！"
echo ""
echo "  【Windowsで実行】"
echo "  git pull"
echo ""
echo "  【KDPアップロード後にWindowsで実行】"
echo "  cd c:/dev/devSideHustleCorp/04_KDP_Automation"
echo "  git rm output/*.epub output/*.jpg output/KDP_upload_info.md"
echo "  git commit -m '[KDP] epub・表紙・投稿情報をGit管理から除外'"
echo "  git push"
echo ""
