# LEARNINGS.md — 学習ループログ

> セッション中に発見した「うまくいったこと・失敗・パターン」を記録する。
> 週次または節目ごとにClaudeが合成し、重要な原則は CLAUDE.md へ昇格させる。
>
> **フォーマット**
> - 観察: 発見した事実（日付付き）
> - 合成: 複数の観察から導き出された原則（週次レビュー時に記入）
> - 昇格済み: CLAUDE.md に組み込んだもの（アーカイブ）

---

## 観察ログ

### 2026-04-11

**[失敗] writer.py が trend_guide.json を半分しか使っていなかった**
- trending_topics: 全5件中3件のみ渡していた
- hook_phrases: 全7件中3件のみ渡していた
- post_patterns: 全3件中1件のみ、かつ例文を60字で切り捨てていた
- avoid_patterns: 全4件中2件のみ渡していた
- hashtags: 完全に未使用だった
- → `agents/writer.py` を修正して全件渡すよう改善（commit: 70f9397）

**[発見] バズサーチ（trend_researcher.py）の自動実行に証跡がない**
- Mac側でlaunchd経由で動いているが、logsディレクトリが存在しない
- trend_guide.json の updated_at を見るしかなく、正常終了か異常終了かが判別できない
- → ログ確認の習慣と、異常時の検知方法を要検討

**[改善] Claude Code の許可設定を bypassPermissions に変更**
- 毎回の確認プロンプトがオーナーの作業を中断していた
- `~/.claude/settings.json` に `"defaultMode": "bypassPermissions"` を設定
- → 以降の作業で確認なしにツール実行可能

---

### 2026-04-12

**[決定] KDP出版ペースを週2回（木曜・日曜 23:00）に設定**
- 週1では積み上げが遅い。週2がアカウントリスクなく現実的なスイートスポット
- 週5以上はAmazonのスパム判定リスクあり
- launchd plist を配列形式で木曜・日曜の2トリガーに変更・反映済み

**[実装] Google Tasks完全連携を追加**
- main.py: 本生成後に「[KDP] アップロード「タイトル」」TODOを自動追加
- record_asin.py: ASIN記録後に該当Google Tasksタスクを自動完了
- pending_upload が複数ある場合はMULTIPLE_PENDINGを出力→Claudeがタイトルを確認する設計

**[運用] ASIN登録フローをチャット完結に変更**
- オーナーがASINをチャットに貼る → Claudeが record_asin.py 実行 → Google Tasks完了まで一括処理
- pending が1件なら自動特定、複数ならタイトルを確認する

**[検討] 洋書KDP（英語）への展開**
- パイプラインはプロンプト変更だけで対応可能（技術的障壁ほぼゼロ）
- 日本語KDPで収益モデルを検証してから並走を判断する方針
- 「日本関連コンテンツ」ジャンルは競合少・強み活かせる有望ニッチ

**[バグ] analyst_feedback.jsonのhour_statsはUTC時間で集計される**
- poster.pyはpost_timesをJSTとして解釈するため、そのまま使うと9時間ずれる
- optimize_post_times.pyでUTC→JST変換（+9時間）が必須
- 今後 analyst.py を改修する場合もこの仕様に注意

**[構造] Threadsのconfig.jsonは旧環境(/Users/seidai/threads_bot/)から移行が必要だった**
- サブモジュール(01_Threads_Automation/)にconfig.jsonが存在せず、auto_optimize等が動かない状態だった
- /Users/seidai/threads_bot/config.json をサブモジュールにコピーして解決
- 今後の新規Macセットアップ時も同様の移行が必要

**[設計] post_timesはlaunchd起動時刻と必ず合わせること**
- poster.pyは起動時刻から±30分以内のpost_timesしか実行しない
- launchd起動時刻: 8:25/11:55/20:55 JST → post_timesは 09:00/12:00/21:00 が正解
- optimize_post_times.pyにLAUNCHD_HOURS_JST=[9,12,21]制約を追加済み
- launchd起動時刻を変更した場合は必ずLAUNCHD_HOURS_JSTも更新すること

---

### 2026-04-13〜14

**[失敗] kill_switch + config.json削除で丸一日投稿停止**
- git pull で `config.json` が削除された（.gitignoreに移行されたため）
- かつ `kill_switch.json: active: true` のまま放置されていた
- → セッション開始時に kill_switch と config.json の存在を必ず確認するルールを追加

**[失敗] account_h の混同**
- account_h はれな→水無月 澪に変更されたが、コード側でれなのキューを水無月 澪として処理しようとした
- → アカウント操作前に config.json の該当エントリを Read で確認するルールを追加

**[ルール] 作業終了時は必ずプッシュしてからメモを書く**
- 作業終了の申告を受けても、変更があれば自発的に git push を完了させる
- プッシュ → メモ更新 → 終了報告の順を守る

**[新機能] account_h（水無月 澪 / @mio.minazuki）追加・初回投稿完了**
- genre: spiritual、投稿パターン: empathy/insight/note_lead のローテーション
- spiritual_writer.py を新規作成（RSS不要・Claude APIで直接生成）
- リプライ必須品質チェックを通すため、全パターンにリプライ生成を追加
- note URL: https://note.com/mio_minazuki

**[KDP] Google Tasks連携をMacで初回認証完了（2026-04-13）**
- credentials: `99_System_Logs/google_credentials.json`（gitignore）
- token: `99_System_Logs/google_token.json`（gitignore）
- Macで再認証が必要な場合: `cd 99_System_Logs && python3 google_tasks_sync.py`

---

## 合成ログ（週次レビュー時に記入）

*まだ合成なし — 2026-04-11 観察開始*

---

## 昇格済み（CLAUDE.md反映済み）

*まだなし*

---

*初版作成: 2026-04-11 | AI統括マネージャー*
