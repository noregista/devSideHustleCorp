# MAC_PENDING_TASKS.md — Mac側で実行する保留タスク

> このファイルは **Windows側のClaude Codeが書き込み、Mac側のClaude Codeが実行する** 申し送り。
> Mac側は `git pull` 後にこのファイルを確認し、未完了タスクを実行する。
> **完了したタスクはチェックを付け、全タスク完了後はこのファイルを空（タスクなし状態）に戻してコミットする。**

---

## 未実行タスク

（なし）

---

## 完了履歴
- [x] 2026-06-18 KDP自動化・Threads自動化の停止と撤去
  - LaunchAgent `com.devSideHustleCorp.kdp_main` を停止・plist削除（※申し送り記載の `kdp_automation`/`threads_bot`/`auto_retry` は本Macに存在せず、実ラベルは `kdp_main` だった）
  - ローカルフォルダ `01_Threads_Automation`・`04_KDP_Automation` を撤去
  - 稼働継続: `com.seidai.threads_bot`・`com.maildigest.weekly`（撤去対象外）
