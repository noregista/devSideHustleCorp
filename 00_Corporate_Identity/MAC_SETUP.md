# Mac セットアップ指示書

> このドキュメントを読んでいるということは、Macでこのプロジェクトを始めようとしている。
> 上から順番に実行すれば完了する。所要時間：約20分。

---

## 前提確認

このプロジェクトは以下の構成で動いている：

```
GitHub: devSideHustleCorp  ← 会社全体の管理リポジトリ
    └── 01_Threads_Automation/  ← threads_bot（submodule）
GitHub: threads_bot         ← Threads自動投稿Bot本体
```

---

## Step 1: Homebrew のインストール（未インストールの場合のみ）

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

インストール済みの場合はスキップ。

---

## Step 2: Python 3.10+ の確認

```bash
python3 --version
```

3.10未満の場合：
```bash
brew install python@3.12
```

---

## Step 3: Git の確認

```bash
git --version
```

インストールされていない場合：
```bash
brew install git
```

---

## Step 4: 作業ディレクトリの作成と会社リポジトリのクローン

```bash
mkdir -p ~/dev
cd ~/dev
git clone https://github.com/noregista/devSideHustleCorp.git
cd devSideHustleCorp
```

> ※ GitHubのユーザー名・リポジトリ名は実際のものに合わせて変更してください。

---

## Step 5: サブモジュール（threads_bot）の初期化

```bash
git submodule update --init --recursive
```

これで `01_Threads_Automation/` に threads_bot のコードが展開される。

---

## Step 6: threads_bot の設定ファイルを作成

```bash
cd ~/dev/devSideHustleCorp/01_Threads_Automation

# テンプレートからコピー
cp config.example.json config.json
```

`config.json` を開いて以下を設定する：

```bash
open -e config.json   # テキストエディタで開く
```

設定が必要な項目：
- `app_id` — Meta App ID
- `anthropic_api_key` — Anthropic API Key
- `fal_key` — fal.ai API Key
- `accounts[*].long_lived_token` — 各アカウントのアクセストークン
- `accounts[*].threads_user_id` — Threads User ID

> ⚠️ config.json は .gitignore されているため、GitHubにはpushされない。
> Windows側のconfig.jsonを参照して手動でコピーすること。

---

## Step 7: 依存パッケージのインストール

```bash
cd ~/dev/devSideHustleCorp/01_Threads_Automation
pip3 install anthropic
```

video系機能（room_tour）を使う場合は追加で：
```bash
pip3 install moviepy Pillow
```

---

## Step 8: 動作確認（dry_runモード）

`config.json` の `dry_run` が `true` であることを確認してから実行：

```bash
cd ~/dev/devSideHustleCorp/01_Threads_Automation
python3 main.py
```

ターミナルに投稿内容が表示されれば成功（実際には投稿されない）。

---

## Step 9: 自動実行スケジュールの設定（launchd）

Macでは `cron` の代わりに `launchd` を使う。

### plist ファイルの作成

```bash
cat > ~/Library/LaunchAgents/com.devSideHustleCorp.threads_bot.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.devSideHustleCorp.threads_bot</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/あなたのユーザー名/dev/devSideHustleCorp/01_Threads_Automation/main.py</string>
    </array>

    <key>WorkingDirectory</key>
    <string>/Users/あなたのユーザー名/dev/devSideHustleCorp/01_Threads_Automation</string>

    <key>StartCalendarInterval</key>
    <array>
        <dict><key>Hour</key><integer>8</integer><key>Minute</key><integer>25</integer></dict>
        <dict><key>Hour</key><integer>11</integer><key>Minute</key><integer>55</integer></dict>
        <dict><key>Hour</key><integer>20</integer><key>Minute</key><integer>55</integer></dict>
    </array>

    <key>StandardOutPath</key>
    <string>/Users/あなたのユーザー名/dev/devSideHustleCorp/01_Threads_Automation/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/あなたのユーザー名/dev/devSideHustleCorp/01_Threads_Automation/logs/launchd_error.log</string>

    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF
```

`あなたのユーザー名` を実際のMacユーザー名に置き換える：
```bash
whoami  # ← これがユーザー名
```

### launchd に登録

```bash
launchctl load ~/Library/LaunchAgents/com.devSideHustleCorp.threads_bot.plist
```

### 登録確認

```bash
launchctl list | grep devSideHustleCorp
```

---

## Step 10: auto_retry（30分ごとのリトライ）の設定

```bash
cat > ~/Library/LaunchAgents/com.devSideHustleCorp.auto_retry.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.devSideHustleCorp.auto_retry</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/あなたのユーザー名/dev/devSideHustleCorp/01_Threads_Automation/auto_retry.py</string>
    </array>

    <key>WorkingDirectory</key>
    <string>/Users/あなたのユーザー名/dev/devSideHustleCorp/01_Threads_Automation</string>

    <key>StartInterval</key>
    <integer>1800</integer>

    <key>StandardOutPath</key>
    <string>/Users/あなたのユーザー名/dev/devSideHustleCorp/01_Threads_Automation/logs/auto_retry.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/あなたのユーザー名/dev/devSideHustleCorp/01_Threads_Automation/logs/auto_retry_error.log</string>
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.devSideHustleCorp.auto_retry.plist
```

---

## 日常の使い方（同期フロー）

### Windows → Mac に変更を反映する

```bash
cd ~/dev/devSideHustleCorp
git pull
git submodule update --remote
```

### Mac → Windows に変更を反映する

Mac側でコードを変更したら：
```bash
cd ~/dev/devSideHustleCorp/01_Threads_Automation
git add .
git commit -m "変更の説明"
git push

cd ~/dev/devSideHustleCorp
git add 01_Threads_Automation
git commit -m "[threads_bot] サブモジュール更新"
git push
```

Windows側で `git pull && git submodule update --remote` を実行。

---

## トラブルシューティング

### launchd が動いていない

```bash
# 状態確認
launchctl list | grep devSideHustleCorp

# 再起動
launchctl unload ~/Library/LaunchAgents/com.devSideHustleCorp.threads_bot.plist
launchctl load ~/Library/LaunchAgents/com.devSideHustleCorp.threads_bot.plist
```

### アラートの確認

```bash
cat ~/dev/devSideHustleCorp/01_Threads_Automation/logs/launchd_error.log
```

### kill_switch のリセット

```bash
echo '{"active": false}' > ~/dev/devSideHustleCorp/01_Threads_Automation/kill_switch.json
```

---

*作成: 2026-04-10 | devSideHustleCorp AI統括マネージャー*
