#!/bin/bash
# =============================================================
# devSideHustleCorp — Mac セットアップ ワンショットスクリプト
# 使い方: bash mac_setup.sh
# =============================================================
set -euo pipefail

# ── 色付きログ ──────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✓ $*${NC}"; }
info() { echo -e "${YELLOW}▶ $*${NC}"; }
err()  { echo -e "${RED}✗ $*${NC}"; exit 1; }

echo ""
echo "=================================================="
echo "  devSideHustleCorp — Mac セットアップ"
echo "=================================================="
echo ""

# ── Step 1: Homebrew ────────────────────────────────────────
info "Homebrew を確認中..."
if ! command -v brew &>/dev/null; then
  info "Homebrew をインストール中..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  ok "Homebrew はインストール済み"
fi

# ── Step 2: Python 3.10+ ─────────────────────────────────
info "Python を確認中..."
PYTHON=""
for cmd in python3.12 python3.11 python3.10 python3; do
  if command -v "$cmd" &>/dev/null; then
    VER=$("$cmd" -c "import sys; print(sys.version_info[:2])")
    if "$cmd" -c "import sys; assert sys.version_info >= (3,10)" 2>/dev/null; then
      PYTHON="$cmd"
      ok "Python: $($cmd --version)"
      break
    fi
  fi
done
if [ -z "$PYTHON" ]; then
  info "Python 3.12 をインストール中..."
  brew install python@3.12
  PYTHON="python3.12"
fi

# ── Step 3: Git ───────────────────────────────────────────
info "Git を確認中..."
if ! command -v git &>/dev/null; then
  brew install git
fi
ok "Git: $(git --version)"

# ── Step 4: git config ───────────────────────────────────
info "Git ユーザー設定を確認中..."
if [ -z "$(git config --global user.email 2>/dev/null)" ]; then
  git config --global user.email "noregista@gmail.com"
  git config --global user.name "noregista"
  ok "Git ユーザー設定完了"
else
  ok "Git ユーザー設定済み: $(git config --global user.email)"
fi

# ── Step 5: リポジトリのクローン ─────────────────────────
WORK_DIR="$HOME/dev/devSideHustleCorp"
info "リポジトリを確認中: $WORK_DIR"
if [ -d "$WORK_DIR/.git" ]; then
  ok "リポジトリ存在済み — git pull を実行"
  git -C "$WORK_DIR" pull
else
  mkdir -p "$HOME/dev"
  info "devSideHustleCorp をクローン中..."
  git clone https://github.com/noregista/devSideHustleCorp.git "$WORK_DIR"
fi

# ── Step 6: サブモジュール（threads_bot）の初期化 ─────────
info "サブモジュール (threads_bot) を初期化中..."
git -C "$WORK_DIR" submodule update --init --recursive
ok "サブモジュール展開完了"

# ── Step 7: 依存パッケージのインストール ─────────────────
BOT_DIR="$WORK_DIR/01_Threads_Automation"
info "依存パッケージをインストール中..."
$PYTHON -m pip install --quiet --upgrade pip
$PYTHON -m pip install --quiet anthropic
ok "anthropic インストール完了"

# ── Step 8: config.json の確認 ───────────────────────────
if [ ! -f "$BOT_DIR/config.json" ]; then
  cp "$BOT_DIR/config.example.json" "$BOT_DIR/config.json"
  echo ""
  echo -e "${YELLOW}=================================================="
  echo "  ⚠️  config.json を設定してください"
  echo "=================================================="
  echo "  以下を編集して、実際のトークンを入力してください:"
  echo "  $BOT_DIR/config.json"
  echo ""
  echo "  設定が必要な項目:"
  echo "  - anthropic_api_key"
  echo "  - fal_key"
  echo "  - accounts[*].long_lived_token"
  echo "  - accounts[*].threads_user_id"
  echo -e "==================================================${NC}"
  echo ""
  read -p "  config.json の設定が終わったら Enter を押してください..."
else
  ok "config.json 存在確認済み"
fi

# ── Step 9: logs ディレクトリの作成 ──────────────────────
mkdir -p "$BOT_DIR/logs"
ok "logs ディレクトリ作成"

# ── Step 10: dry_run で動作確認 ───────────────────────────
info "dry_run モードで動作確認中..."
DRY=$(python3 -c "import json; c=json.load(open('$BOT_DIR/config.json')); print(c.get('dry_run', True))")
if [ "$DRY" != "True" ]; then
  echo -e "${YELLOW}  ⚠️  config.json の dry_run が false です。テストのため一時的に true に変えてください。${NC}"
else
  cd "$BOT_DIR" && $PYTHON main.py && ok "dry_run テスト完了"
fi

# ── Step 11: launchd の登録 ──────────────────────────────
USERNAME=$(whoami)
PLIST_DIR="$HOME/Library/LaunchAgents"
mkdir -p "$PLIST_DIR"

info "launchd (main bot) を登録中..."
cat > "$PLIST_DIR/com.devSideHustleCorp.threads_bot.plist" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.devSideHustleCorp.threads_bot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$BOT_DIR/run_with_pull.sh</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$BOT_DIR</string>
    <key>StartCalendarInterval</key>
    <array>
        <dict><key>Hour</key><integer>8</integer><key>Minute</key><integer>25</integer></dict>
        <dict><key>Hour</key><integer>11</integer><key>Minute</key><integer>55</integer></dict>
        <dict><key>Hour</key><integer>20</integer><key>Minute</key><integer>55</integer></dict>
    </array>
    <key>StandardOutPath</key>
    <string>$BOT_DIR/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>$BOT_DIR/logs/launchd_error.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
PLIST

info "launchd (auto_retry) を登録中..."
cat > "$PLIST_DIR/com.devSideHustleCorp.auto_retry.plist" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.devSideHustleCorp.auto_retry</string>
    <key>ProgramArguments</key>
    <array>
        <string>$(which $PYTHON)</string>
        <string>$BOT_DIR/auto_retry.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$BOT_DIR</string>
    <key>StartInterval</key>
    <integer>1800</integer>
    <key>StandardOutPath</key>
    <string>$BOT_DIR/logs/auto_retry.log</string>
    <key>StandardErrorPath</key>
    <string>$BOT_DIR/logs/auto_retry_error.log</string>
</dict>
</plist>
PLIST

launchctl load "$PLIST_DIR/com.devSideHustleCorp.threads_bot.plist" 2>/dev/null || true
launchctl load "$PLIST_DIR/com.devSideHustleCorp.auto_retry.plist" 2>/dev/null || true
ok "launchd 登録完了"

# ── 完了 ─────────────────────────────────────────────────
echo ""
echo "=================================================="
echo -e "${GREEN}  ✓ セットアップ完了！${NC}"
echo "=================================================="
echo ""
echo "  プロジェクト: $WORK_DIR"
echo "  Bot本体:     $BOT_DIR"
echo ""
echo "  【日常の同期コマンド】"
echo "  cd $WORK_DIR"
echo "  git pull && git submodule update --remote"
echo ""
echo "  【手動実行】"
echo "  cd $BOT_DIR && $PYTHON main.py"
echo ""
echo "  【緊急停止】"
echo "  echo '{\"active\": true}' > $BOT_DIR/kill_switch.json"
echo ""
