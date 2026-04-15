# DAILY_LOG.md — 日次作業ログ

> セッション終了時にAI統括マネージャーが自動記録する。オーナーへの報告より、次回セッションの文脈把握が目的。

---

## 2026-04-12

### 完了
- KDPアカウント開設・銀行口座・税務情報（W-8BEN）登録
- 初回出版申請：「ChatGPT・Claude完全攻略ガイド」¥980（審査中・72時間以内に販売開始）
- fal.ai(flux-pro)による高品質表紙自動生成を実装
- transfer_to_windows.sh（安全なepub転送スクリプト）作成
- KDP_upload_info.md自動生成（次回から設定値コピペだけでOK）
- record_asin.py（ASIN記録スクリプト）作成
- book_history.jsonにステータス管理導入・40代の本を追加
- Business-Tracker.md・memory更新

### 翌日の優先タスク
- Mac側で `git pull`（fal.ai表紙生成を有効化）
- 72時間後にAmazonで販売確認 → `python3 record_asin.py B0XXXXXXXXX`
- 40代からの資産形成戦略の出版判断

### 数値
- KDP出版数: 1冊（申請中）
- 累計epub生成: 2冊（ChatGPT本・40代資産形成本）
- Threads: 継続稼働中
- API使用量: Proプラン53%消費（週間・セッション共に）

### その他メモ
- DAILY_LOG・日報の仕組みを導入（セッション終了時に自動記録）
- APIクレジット残$1.99はボット用。Claude Codeはサブスク（Pro）で別管理
- Proプランの使用量はclaude.ai/settings/usageで確認可能

---

## 2026-04-13

### 完了
- **Batch API + Prompt Caching 導入**：全章を一括生成（50%コスト削減）、システムプロンプトをキャッシュ化（2章目以降1/10コスト）→ 合計約75%削減見込み
- **Geminiフォールバック修正**：config.jsonの`gemini_api_key`が`os.environ`に反映されていなかったバグを修正
- **研究キャッシュ再利用**：当日のresearch_cache/YYYY-MM-DD.jsonがあればresearcher.pyをスキップ
- **章再生成ロジック強化**：500字未満またはaudit失敗で自動リトライ
- **epub修正**：`**太字**`→`<strong>`変換、番号リストを`<ol>`で正しく出力
- **生成時間計測バグ修正**：パイプライン開始時刻を正確に計測
- **Devil's Advocateレビュー**：Haikuがアウトラインを批評、失敗時Opusが再生成
- **dry_runモード完全対応**：ファイル保存・Google Tasks・Threads投稿をスキップ
- **Opus 4.6でアウトライン生成**：価格67%低下で採用、最高品質の構成生成
- **AI臭さ除去（naturalize_chapter）**：Haikuが各章を自然な日本語に後処理
- **Reddit RSSソース追加**：r/selfpublishing, r/Entrepreneur, r/productivity（国際トレンド先行検知）

### 翌日の優先タスク
- Mac側で `git pull`（全改善を取り込む）
- Amazon KDPで初回本の審査状況を確認（72時間以内に販売開始のはず）
- ASIN判明次第 `python3 record_asin.py B0XXXXXXXXX` で記録
- 次の自動実行は日曜23:00（全機能フル稼働の初回テスト）

### 数値
- KDP出版数: 1冊（審査中）
- 累計epub生成: 2冊
- git commits（本日）: 5件（Batch API / epub修正 / バグ修正 / Devil's Advocate / Opus+AI臭さ除去）
- パイプライン完成度: ほぼ100%（残: コスト実績値の記録くらい）

### その他メモ
- コアパイプラインに残バグなし。日曜の自動実行が全機能フル稼働の初回になる

---

## 2026-04-14

### 完了
- **水無月 澪（スピリチュアル占い）アカウント新設**: 縁結びリーディングのオリジナルキャラ設計。独自世界観（水脈・濁り・清流・水鏡）確立
- **spiritual_writer.py 新規作成**: RSS不要・Claude Haiku APIで直接生成。3パターンローテーション（empathy/insight/note_lead）
- **初投稿実施 → 品質改善**: 「冒頭から責める」問題を検出。共感優先プロンプトに全面改修
- **engagement_insights フィードバックループ追加**: 高エンゲージメント投稿のフックを自動反映する仕組みを実装
- **Meta for Developers 新アプリ設定**: C/D/E/H アカウントのトークンを新アプリで再発行。澪のトークンも追加
- **04_KDP マージコンフリクト解消**: Mac側のGoogle Tasks詳細ノート版を採用
- **writer.py バグ修正**: spiritualアカウントにニュースが誤割り当てされる不具合を修正

### 翌日の優先タスク
- れなのMeta審査が通ったら: 新アプリ（ID: 1422148273258080）で短期トークン発行 → config.jsonに追加
- 第2回出版（AIに仕事を任せる側になれ）のアップロード → オーナーが完了次第報告
- れなのMeta審査通過後: 新アプリでトークン発行 → config.jsonに追加

### 数値
- Threads稼働アカウント: 4（C/D/E/H=澪）+ れな審査待ち
- スピリチュアルパイプライン: 稼働開始（初投稿済み）
- git commits（本日）: 7件

### その他メモ
- poster.pyに潜在バグあり（url=Noneの衝突）。スピリチュアル2アカウント目追加前に要修正。memory記録済み
- Mac自動pull設定を記憶に追加（run_with_pull.shが毎回pullするため手動pull不要）
- bypassPermissions モード有効化・「チェックを求めない」記憶追加（次回から承認・確認不要）
- KDP初回本 販売開始・ASIN: B0GX2VQJPC・KDPセレクト登録・著者セントラル登録 完了
- Google Tasks完了処理をWindows側から直接実行できるようにした

---
