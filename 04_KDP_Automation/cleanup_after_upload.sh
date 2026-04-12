#!/bin/bash
# cleanup_after_upload.sh
# KDPアップロード完了後にGitからepubを削除するスクリプト。
# Windows側でのアップロード完了後にMacで実行する。
#
# 使い方:
#   bash cleanup_after_upload.sh

set -euo pipefail

BOT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$BOT_DIR/.." && pwd)"
GITIGNORE="$BOT_DIR/.gitignore"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✓ $*${NC}"; }
info() { echo -e "${YELLOW}▶ $*${NC}"; }
err()  { echo -e "${RED}✗ $*${NC}"; exit 1; }

echo ""
echo "=================================================="
echo "  KDP後処理: Gitからepubを削除"
echo "=================================================="
echo ""

# output/ がGit管理下かチェック
TRACKED=$(git -C "$REPO_DIR" ls-files "04_KDP_Automation/output/" 2>/dev/null | head -1)
if [ -z "$TRACKED" ]; then
  ok "output/ はすでにGit管理外です。作業不要です。"
  exit 0
fi

# Step 1: .gitignore の output/ を有効化
info ".gitignore を復元中（output/ を再び除外）..."
if grep -q '^#output/$' "$GITIGNORE"; then
  sed -i '' 's|^#output/$|output/|' "$GITIGNORE"
  ok ".gitignore 復元完了"
else
  ok ".gitignore はすでに正しい状態です"
fi

# Step 2: Git管理からepubファイルを削除（ローカルファイルは残す）
info "Gitキャッシュから output/ を削除中..."
git -C "$REPO_DIR" rm --cached -r "04_KDP_Automation/output/" 2>/dev/null || true
ok "git rm --cached 完了（ローカルファイルは保持）"

# Step 3: コミット
info "コミット中..."
git -C "$REPO_DIR" add "04_KDP_Automation/.gitignore"
git -C "$REPO_DIR" commit -m "[04_KDP_Automation] epub転送完了後クリーンアップ: output/ をGit管理外に戻す

- .gitignore の output/ コメントアウトを解除
- Git管理から epub/jpg/KDP_upload_info.md を削除（ローカルには残す）

背景: Windows側でのKDPアップロード完了後の後処理"
ok "コミット完了"

# Step 4: プッシュ
info "プッシュ中..."
git -C "$REPO_DIR" push
ok "プッシュ完了"

echo ""
echo "=================================================="
echo -e "${GREEN}  ✓ クリーンアップ完了！${NC}"
echo "=================================================="
echo ""
echo "  次のアクション:"
echo "  1. KDPダッシュボードで審査状況を確認（24〜72時間）"
echo "  2. 出版確定後にASINを記録:"
echo "     cd $BOT_DIR && python3 record_asin.py B0XXXXXXXXX"
echo ""
