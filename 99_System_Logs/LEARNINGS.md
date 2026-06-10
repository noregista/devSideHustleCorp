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

### 2026-04-16

**[整理] アカウントIDをa〜eに統一**
- 旧: account_c=けんた, account_d=みか, account_e=ゆい, account_g=れな, account_h=澪
- 新: account_a=けんた, account_b=みか, account_c=ゆい, account_d=れな, account_e=澪
- 対象: config.json / post_history.json / post_queue.json / engagement_insights.json / pre_post_checker.py

**[失敗] 朝枠の投稿が2アカウントスキップされた**
- researcher が RSS 遅延で15分かかり（lifehacker.jp）、poster 開始が 08:57 にずれ込んだ
- みかの Threads API がレートリミットでリトライし27分かかった（08:57→09:24）
- 09:31 にけんた・ゆいの post_times ±30分窓が閉じていてスキップ
- → poster.py の窓を ±30分 → ±90分 に拡大して修正

**[整理] LaunchAgent を大幅整理**
- com.game_news_bot（14回起動）→ com.seidai.threads_bot（3回: 07:30/11:30/20:30）に変更
- com.gamenewsbot.* 10個（room_tour / auto_retry 等）を全削除
- com.devSideHustleCorp.threads_main（main.py）が run.sh と重複投稿していた → 削除
- 現在稼働: com.seidai.threads_bot のみ

**[設計] 澪（spiritual_writer）の投稿を1日2回に変更**
- 1日1件制限 → 1日2件（朝07:30起動・夜20:30起動で各1件生成）
- post_times: ['08:50', '21:00']（昼枠は削除）

---

### 2026-06-10

**[失敗→修正] Konvaの放射状ライン装飾が「家具」に見えず記号(X字)に見えた**
- 家具レイアウトシミュレーターのchairマーカーで、座面中心から5方向へ伸びる「キャスター脚」を線(Line)で表現したところ、
  小さいサイズで描画すると単なる赤い四角に「X」や星マークが描かれているように見え、椅子に見えなかった
- → 線の放射ではなく、背もたれ・肘掛け・座面クッションを面(Rect)の重なりで表現する方式に変更したところ、
  小サイズでも「椅子」と認識できるようになった
- 教訓: 小さな描画領域では「線の集合」より「面の重なり・濃淡差」の方が形状認識されやすい

**[失敗→修正] rugマーカーが「床の一部」にしか見えなかった**
- 縞模様(横線)だけのrugは床色と近い色でほぼ同化し、カーペットというより木目床や段ボールに見えた
- → 縁取り枠＋中央メダリオン（円の二重マーカー）＋不透明度を0.82→0.88に上げ、色も床と差がつく暖色(#D9A887)に変更
- 教訓: 「敷物」を表現するには色のコントラストだけでなく、中央装飾(メダリオン)のような象徴的パターンが効果的

**[致命的バグ→修正] 専用家具アイコン化リファクタで全家具がクリック選択・ドラッグ不能になっていた**
- react-konvaの `listening` は子孫に継承される。FurnitureObject2Dの「ドロップシャドウ用Rect」に `listening={false}` を付けたまま、
  各Iconコンポーネントも内部で `<Group listening={false}>` を使っていたため、家具グループ内に「listeningな図形」が一つも存在しなくなった
- Konvaの `onClick`/`onTap`/`draggable` は子のlisteningなShapeからのイベントバブリングで発火するため、優先6カテゴリ
  (bed/desk/chair/rug/tv_stand/storage_shelf＝サンプル部屋の全家具)が選択もドラッグも一切できない状態になっていた
- E2Eテスト(13/13)はキャンバスクリックでの選択を一切検証していない（ストア側のauto-selectのみ通過）ため、テストは全通過のまま検出されず、
  スクリーンショットの「選択状態が変わらない」という見た目の違和感で発覚した
- → ドロップシャドウ用Rect (`fill="transparent"`) から `listening={false}` を削除して当たり判定を兼ねさせて修正。
  Konvaは `fill="transparent"` でも `hasFill()` がtruthyなため、見た目は透明のままヒットエリアとして機能する
- 教訓: KonvaのGroup/Shape階層を変更（特にカスタムアイコン化など）した後は、必ず実際のクリック・ドラッグ動作を
  スクリプト等で確認する。「listeningな図形が階層内に最低1つ存在するか」をレビュー観点に加える

**[改善] オーナーレビュー後の「微調整」は、コンポーネント全面刷新ではなくパラメータ調整で対応できた**
- 上記の根本刷新後、オーナーから「チェアの記号感」「ラグの主張過多」「配色がベージュ/テラコッタに寄りすぎ」
  「LPヒーローのアプリ作例感」「CTAボタンの強弱」の5点フィードバックを受けたが、いずれも既存コンポーネントの
  形状パラメータ(cornerRadius・要素配置)・色定数(palette.ts)・Tailwindクラス(状態別スタイル)・レイアウト比率の
  調整のみで解決でき、構造的な作り直しは不要だった
- 各変更点ごとに専用のセルフチェックスクリプト(self-check-chair-zoom.ts, self-check-rug-zoom等, self-check-button.ts)で
  該当箇所だけをクロップしたスクリーンショットを撮り、Readツールで視覚確認してからコミットする流れが有効だった
- 教訓: 「見た目の質感を上げてほしい」という指摘は大改修のサインではなく、まず色・サイズ・余白などの
  パラメータレベルの調整で対応できないか検討する。各修正は対象を絞ったセルフチェック画像で個別に検証する

**[実装] 匿名共有URL機能をhash fragment方式（`/share#data=<encoded>`）で実装**
- オーナーから「`/share/[id]`にパス埋め込みだとサーバーログ・解析ログに圧縮データが残る」との指摘を受け、
  `#data=...`のhash fragment方式に変更。hashはブラウザからサーバーへ送信されないため匿名共有の趣旨に合致する
- packages/sharedにSharedLayoutPayload型+zodバリデーション(items最大50件、寸法/座標に範囲制約)を追加し、
  decode処理(`decodeSharedLayout`)はdecompress失敗・JSON長超過(50KB)・JSON.parse失敗・zod検証失敗のいずれでも
  例外を投げず`null`を返す設計にした。呼び出し側はnullチェックのみでクラッシュしない
- ペイロードには部屋サイズ・家具配置・商品名・寸法・価格・URLのみを含め、レイアウト名やメモ等の個人情報は
  型定義の時点で存在させないことで「入れ忘れ」を構造的に防止した

**[失敗→修正] E2Eで「同じ/shareパス上のhash変更」だけではuseEffectが再実行されなかった**
- `/share#data=<正常データ>`から`page.goto('/share#data=invalid')`へ遷移しても、pathnameが同じため
  Next.jsはsame-document navigationとして扱い、ShareViewコンポーネントがアンマウントされず`useEffect(() => {...}, [])`が
  再実行されなかった。結果、不正hashのテストが「直前の正常な表示」のままでエラー画面を検出できずタイムアウトした
- → テスト中で一度`/simulator`など別パスへ遷移してから`/share#data=invalid`へ遷移することで、
  確実にページがフルリロードされエラー画面が表示されるよう修正
- 教訓: hash fragmentのみで状態を切り替えるページをE2Eでテストする際は、hash変更だけでは
  クライアントコンポーネントが再マウントされない前提でテストを設計する

**[確認] lz-string@1.5.0は`@types/lz-string`なしでそのまま型安全に使える**
- `@types/lz-string@1.5.0`をdevDependenciesに追加したところ`deprecated`警告が出た
- lz-string本体の`typings/lz-string.d.ts`がESM named exportsの型を既に提供しているため、
  `@types/lz-string`は不要。`import { compressToEncodedURIComponent, decompressFromEncodedURIComponent } from 'lz-string'`
  のようにnamed importすれば型チェックが通る

---

## 合成ログ（週次レビュー時に記入）

*まだ合成なし — 2026-04-11 観察開始*

---

## 昇格済み（CLAUDE.md反映済み）

*まだなし*

---

*初版作成: 2026-04-11 | AI統括マネージャー*
