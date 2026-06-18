# MAC_PENDING_TASKS.md — Mac側で実行する保留タスク

> このファイルは **Windows側のClaude Codeが書き込み、Mac側のClaude Codeが実行する** 申し送り。
> Mac側は `git pull` 後にこのファイルを確認し、未完了タスクを実行する。
> **完了したタスクはチェックを付け、全タスク完了後はこのファイルを空（タスクなし状態）に戻してコミットする。**

---

## 未実行タスク

### [ ] 2026-06-18 KDP自動化・Threads自動化の停止と撤去

KDP自動化とThreads自動化をプロジェクトごと廃止した。Windows側ではローカルフォルダを削除済み。
Mac側では以下を実行して、LaunchAgentの停止・plist削除・ローカル残骸の撤去を行う。

```bash
# 1. LaunchAgent を停止・アンロード
PLIST_DIR="$HOME/Library/LaunchAgents"
for label in \
  com.devSideHustleCorp.threads_bot \
  com.devSideHustleCorp.auto_retry \
  com.devSideHustleCorp.kdp_automation
do
  launchctl unload "$PLIST_DIR/$label.plist" 2>/dev/null || true
  rm -f "$PLIST_DIR/$label.plist"
  echo "removed: $label"
done

# 2. 念のため残存ジョブを確認（何も出なければOK）
launchctl list | grep -E "threads_bot|auto_retry|kdp_automation" || echo "LaunchAgent: クリーン"

# 3. ローカルフォルダの撤去（リポ側は削除済みなので pull で消えるが、
#    サブモジュールだったThreadsは残骸が残る場合があるので明示削除）
REPO="$HOME/dev/devSideHustleCorp"   # ← Mac上の実パスに合わせて確認
cd "$REPO"
git submodule deinit -f 01_Threads_Automation 2>/dev/null || true
rm -rf .git/modules/01_Threads_Automation 2>/dev/null || true
rm -rf 01_Threads_Automation 04_KDP_Automation 2>/dev/null || true
echo "ローカル撤去完了"
```

実行後の確認：
- `launchctl list | grep -E "threads|kdp"` で何も出ないこと
- `ls` に `01_Threads_Automation` `04_KDP_Automation` が無いこと

完了したら上の `[ ]` を `[x]` にして、このセクションを削除し、
「## 未実行タスク」の下を「（なし）」に戻してコミットする。

---

## 補足
- GitHubリポジトリ `noregista/threads_bot` は**残す**方針（削除しない）。
- Amazon上に出版された書籍は無し（全書籍 ASIN=None＝未出版）なので、撤去による収益影響なし。
