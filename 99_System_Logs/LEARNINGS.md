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

### 2026-06-11

**[実装] 簡易3Dプレビューを箱型(BoxGeometry)で実装、RoomViewer(2D)と同じ「store非依存・汎用props」設計を踏襲**
- `@react-three/fiber`+`@react-three/drei`+`three`はpackage.jsonに以前から入っていたが未使用だった
- 2D編集データ(cm単位、原点=左上、+y=下)→Three.jsワールド座標(m単位、部屋中心が原点、+Y=上)の変換を
  `apps/web/src/lib/three/coords.ts`に集約。家具は底面が床(y=0)に接するよう中心yを高さの半分に設定
- Room3DSceneはRoomViewer同様に`{ widthCm, depthCm, items: [...] }`等のpropsのみで動く汎用コンポーネントにしたため、
  将来`/share`ページに3D対応を追加する際もコンポーネントの修正なしで再利用できる

**[確認] headless Playwright(chromium)でもWebGL(react-three-fiber)は実際にレンダリングされる**
- `[.WebGL-...]GL Driver Message ... GPU stall due to ReadPixels`という非致命的な警告は出るが、
  `room-3d-canvas`は実際に3D描画され、OrbitControlsのドラッグ操作も機能した(エラーフォールバックには落ちなかった)
- E2Eでは`[data-testid="room-3d-canvas"], [data-testid="room-3d-error"]`のいずれかが表示されればpass、
  という両対応セレクタにしておくと、WebGL利用可否が異なる実行環境でも安定する

**[構造] `scripts/`ディレクトリはpnpmワークスペース外。tsx実行は`./node_modules/.bin/tsx`を直接呼ぶ**
- `pnpm-workspace.yaml`は`packages: ["apps/*", "packages/*"]`のみで`scripts/`(`@fls/scripts`)を含まない
- `npx tsx`や`pnpm --filter @fls/scripts exec tsx`はどちらも失敗する
- `scripts/`配下には独自の`node_modules`があるため、`cd scripts && ./node_modules/.bin/tsx <file>.ts`で実行する
- ただし`cd scripts && pnpm run verify-keepa`（`pnpm run`、`--filter`なし）は`scripts/node_modules/.bin/tsx`がPATHに通るため正常に動作する。READMEのKeepa検証手順はこの形式で記載済みで問題なし

**[方針確認] 「3D」を訴求する際は常に「簡易3D」と表記し、過大評価しない**
- オーナーから「現状の3Dは売りになる高品質3Dではなく、高さ感をざっくり確認する簡易プレビュー」という明確な位置づけ指定があった
- View3DToggleのラベル・ローディング表示・エラーフォールバック文言を全て「簡易3D」に統一(`apps/web/src/components/editor/View3DToggle.tsx`等)
- 今後LPに3D訴求セクションを追加する場合も、このトーン(簡易3D=高さ確認用)を踏襲すること

**[発見] MockProviderは未知ASINに対し「モック商品(ASIN)」+疑似乱数寸法を返し、「要確認」バッジのみで配置をブロックしない**
- `apps/api/src/services/product-data/mock.provider.ts`の`getByAsin`は、`MOCK_DATA`にない実在ASINに対してもダミーの商品名・寸法を返す(`needsUserConfirmation: true`)
- `ProductCard.tsx`では「要確認」の小バッジ表示のみで、「部屋に置く」操作は通常通り可能
- KEEPA_API_KEY未設定のままURL入力機能を公開すると、ユーザーに偽の商品情報を見せてしまう。release-checklist.mdにリリースブロッカー候補として記録した

**[コピーレビュー] 「Amazon URLから自動取得」は現状機能を超えた表現だった**
- `layout.tsx`のmeta description・LPのSTEPS[0]descが、未実装のKeepa自動取得をあたかも現状機能のように記述していた
- 「家具サイズを入力して部屋に置けるか確認」を主訴求にし、URL欄は「商品メモ・将来の自動取得予定」という補助的な位置づけに修正
- 今後コピーを書く際は、未実装機能を「対応予定」と書く場合でも、それが主訴求文の冒頭に来ないようにする(主訴求=現状動く機能であるべき)

**[実装] 「人のスケール」機能（複数人・姿勢対応）を`people?: PersonInstance[]`の独立配列として実装**
- オーナーの最終仕様確認で「自分を置く」(1人・診断/アバター的)案から「人のスケール」(複数人・実用)案に変更。
  位置づけは「家具サイズ・通路幅・座る/寝るスペース確認のための実用機能」であり、診断・ゲーム性・アバター・体型/性別/服装/顔/写真は一切含めない方針
- `PersonInstance`は`furniture[]`(家具)とは完全に別の型・別配列とし、`LayoutData`/`SharedLayoutPayload`に
  `people?: PersonInstance[]`としてoptional追加。`people`キーが無い既存の保存データ・既存の`/share#data=...`リンクは
  そのまま`safeParse`/JSONパースに通り後方互換が保たれる
- 姿勢(standing/sitting/lying)ごとにフットプリント(`getPersonFootprintCm`)を分離: standing/sittingは身長によらず固定サイズ、
  lyingのみ`widthCm: heightCm`として身長がそのまま床面の長さに反映される。2D(react-konva)・3D(@react-three/fiber)の両方で
  この単一関数を共有することで見た目の整合性を担保した
- 3Dの「寝た人がベッド上にいれば高さ分かさ上げ・座った人が椅子上にいれば座面高さで表示」は、`RoomCanvas2D`の
  ドラッグクランプで使っていたcos/sin半幅・半高のAABB式をそのまま`getPersonSurfaceHeightCm`に再利用して実装(「簡易的」と明記)。
  既存の回転矩形あたり判定ロジックは流用できる場面が多い
- 3Dモデルは仕様通り`cylinderGeometry`+`sphereGeometry`の組み合わせのみで構成し`capsuleGeometry`は未使用
  (型・互換性リスク回避が目的で、見た目のリアルさは目的外)
- UI実装時、PersonSizeCard(リスト行の削除ボタン)とPropertiesPanel(選択中人物パネルの削除ボタン)が同時に
  画面上に存在しうるため、testidを`person-list-remove-button`/`remove-person-button`で意図的に分けて衝突を回避した
- E2Eを17→23件に拡張(人物追加/複数人/姿勢切替/保存復元/共有リミックス復元/上限4人ブロック)、型チェック・全件pass

**[修正] 「人のスケール」オーナーレビュー後の4点フィードバック対応完了**
- standing(立つ)が「ベッドの上に立っている」ように見えた原因は、`getPersonSurfaceHeightCm`の高さ計算ではなく
  (standingは元から常に0=床基準を返す実装だった)、`addPerson()`のデフォルト配置座標(50,50)/(80,80)が
  サンプルベッドのAABB(x:[5,105], y:[5,200])と重なっていたこと。床基準の人物が不透明なベッド箱(高さ35cm)に
  下半身を隠され「ベッドに立っている」ように見えていた
- → 新規ヘルパー`findFreeStandingPositionCm`(20cm刻みでグリッド探索)を追加し、`addPerson()`で
  希望位置が家具と重なる場合は空いている床上の位置を自動選択するよう修正。高さ計算ロジック自体は変更不要だった
- 教訓: 「3D表示が不自然」という指摘を受けたら、まず高さ計算ロジックを疑う前に、デフォルト配置座標と
  既存家具のAABBが重なっていないか(視覚的なオクルージョン)を確認する
- 共有URL長すぎエラー文言を「家具数が多すぎるため共有URLを作成できません」→
  「共有URLが長すぎます。家具・人・商品名を減らしてください。」に変更(原因を限定しすぎないように)
- 2D人物アイコン(PersonIcon2D)に`isSelected`propを追加し、非選択時は不透明度0.5〜0.7・ラベル縮小で
  家具の視認性を妨げないよう調整(lyingは特に控えめ=0.5)
- 3D人物モデル: standingの胴体をテーパー円柱で細く、頭身比率(PERSON_HEAD_RATIO 0.13→0.12)を自然に、
  配色を`PERSON_COLOR`(#8CA3B3)/`PERSON_COLOR_DARK`(#5E7A8C)の落ち着いたグレイッシュブルー2色に変更、
  sittingに左右の脚(太もも+すね、計4本のcylinder)を追加して着座姿勢を分かりやすくした
- 既存の`scripts/self-check-people.ts`でエラー文言変更(上記)に追従していないアサーションがあり検出漏れになりかけた。
  教訓: エラー文言を変更したら、その文言を直接アサートしているセルフチェック/E2Eを横断検索して追従させること
- type-check pass・E2E 23/23 pass・self-check-people.ts全項目OK確認後、commit: 21827e5・push済み

**[致命的バグ→修正] `/simulator`が画面幅576px以下で完全クラッシュしていた根本原因と修正パターン**
- 左サイドバー(`w-80`=320px)+右パネル(`w-64`=256px)=576pxの固定幅消費により、ビューポート幅576px以下では
  中央`canvas-area`の幅が0以下になり、react-konvaの`Stage`が`width/height 0`のcanvasに`drawImage`して
  `InvalidStateError`が発生。Next.jsのエラーバウンダリに捕捉され、画面がほぼ無地になっていた(前回visual reviewで発見)
- → 修正は「0サイズで描画しない」だけでなく、**768px未満は編集UI自体をマウントしない**という2段構えにした:
  1. `SimulatorMobileFallback`(新規)を作り、768px未満は`SimulatorLayout`の早期returnでPC/タブレット推奨画面のみ表示。
     `RoomCanvas2D`/`Room3DScene`は`dynamic(..., { ssr:false })`経由のため、マウントしなければKonva/ThreeのCanvas自体が生成されない
  2. `useElementSize`(新規、ResizeObserver+useLayoutEffect)で実寸を計測し、0以下の間は`Stage`/`Canvas`を
     描画せず「画面サイズを広げてください」を表示(768px以上でも理論上の防御として機能)
- 768pxの判定は`window.matchMedia('(max-width: 767px)')`を使い、`isMobile: boolean | null`の3値管理(`null`=判定前)で
  SSR/初回クライアントレンダリングの両方を同じ中立な空div(`<div className="h-screen bg-ivory" />`)に倒すことで
  ハイドレーション不一致を回避した
- 教訓: 「0サイズでcrashするコンポーネントを直す」だけでなく、「そもそもそのブレークポイントでは別のUIに切り替える」
  という設計の方が、未対応のモバイル編集UIを段階的に作る前段としても適切な場合がある

**[ハマりどころ] JSX内の条件分岐でラップする際、開きタグと閉じタグの対応をRead確認せず編集すると壊れる**
- RoomCanvas2Dの`<Stage>...</Stage>`をサイズガード付きの三項演算子`{cond ? (<placeholder/>) : (<Stage>...)}`で
  ラップする際、最初の編集で開きタグ側だけ変更し、対応する`</Stage>`(+Fragment閉じ)を追従させなかったため、
  `</Stage>`が二重に残ってJSXが壊れた
- → Readで実際の行番号・構造を確認してから、開きタグ側の追加と閉じタグ側の追加をペアで編集することで修正
- 教訓: 複数行にまたがるJSX要素を条件分岐でラップする編集は、1回のEditで開閉両方を変更するか、
  必ず編集直後にReadで構造を確認する

**[ハマりどころ] Playwrightの`reuseExistingServer: true`は、既存サーバー起動時に新しい`webServer.env`を反映しない**
- `playwright.config.ts`の`webServer.env`に`NEXT_PUBLIC_ENABLE_URL_IMPORT: 'false'`を追加したが、
  ポート3000に前回セッションから起動したままの`pnpm dev`サーバーが残っており、`reuseExistingServer: !process.env.CI`(devでは true)
  によりPlaywrightがそれをそのまま再利用し、新しい環境変数が適用されなかった
- → `Get-CimInstance Win32_Process`等で該当PIDのプロセスを確認後`Stop-Process -Force`し、ポートを空けてから
  `playwright test`を実行することで、新しい`env`付きでサーバーが再起動され反映された
- 教訓: `webServer.env`を変更した場合、devモードでは既存の起動中サーバーが残っていないか確認し、
  残っていれば一度落としてから`playwright test`を実行する(でないと変更が無視されたままテストがpassしてしまう)

**[致命的バグ→修正] root `layout.tsx`のグローバル`robots: { index: false, follow: false }`が全ページをnoindexにしていた**
- favicon/OGP整備のためroot `layout.tsx`を確認したところ、`metadata.robots`に`{ index: false, follow: false }`がグローバル設定されていた
- `/page.tsx`(LP)は独自の`metadata`を持たないためroot設定をそのまま継承し、**公開予定のLP `/`までnoindexになっていた**
- `/simulator`・`/share`は元々ページ個別に同じ`robots`を設定済みだったため実害は無かったが、設定意図(個別ページのnoindex)とroot設定(全体noindex)が重複・混在していた
- → root `layout.tsx`から`robots`キー自体を削除(Next.jsのデフォルト=`index, follow`)。`/simulator`・`/share`はページ個別の`robots`設定でnoindexを維持(Next.jsのmetadataマージはトップレベルキー単位の上書きのため、個別設定はrootの変更の影響を受けない)
- 教訓: 「個別ページをnoindexにしたい」場合でも、rootレイアウトに`robots`を置くと**それ以外の全ページに波及する**。ページ固有の制御は必ずそのページの`metadata`で行い、root側はサイト全体のデフォルト(通常は未設定=index許可)に留める

**[制約] `next/og`(Satori)は日本語フォントを標準搭載しないため、favicon/OGP画像はテキストなしの図形のみで構成した**
- `next/og`の`ImageResponse`は内部で`@vercel/og`(Satori)を使うが、デフォルトで同梱されるフォントはラテン文字のみ(`noto-sans-v27-latin-regular.ttf`)
- 日本語テキストを描画するには`fonts`オプションでCJKフォントのバイナリを別途`fetch`/読み込みする必要があり、ビルド時の追加依存・オフラインビルド失敗リスクが増える
- → favicon(`icon.tsx`)・apple-icon・OGP/Twitter画像(`opengraph-image.tsx`/`twitter-image.tsx`)は全てWarm Editorialパレットの図形(角丸・色面によるアイコンマーク/簡易フロアプラン)のみで構成し、テキストを一切使わない設計にした
- サービス名・説明文はSNS側が`<meta property="og:title">`/`<meta property="og:description">`(通常のHTML metaタグ、Satori非経由)から表示するため、日本語タイトルは問題なく表示される
- 教訓: `next/og`で日本語を含む画像が必要になった場合は、フォント同梱のコスト(ビルド時間・依存関係)と、テキストを使わない図形デザインで代替できないかを先に検討する

**[ハマりどころ→修正] `next/og`のNode runtime(デフォルト)はWindows上で`next build`が"Invalid URL"エラーになる**
- `icon.tsx`/`apple-icon.tsx`/`opengraph-image.tsx`/`twitter-image.tsx`を作成し`next build`したところ、
  4ルート全てで`TypeError: Invalid URL` (`fileURLToPath`内、`@vercel/og/index.node.js`)が発生しビルド失敗した
- 原因: `index.node.js`が`fs.readFileSync(fileURLToPath(join(import.meta.url, "../noto-sans-v27-latin-regular.ttf")))`という形でデフォルトフォントを読み込むが、
  `path.join`はWindowsでは区切り文字に`\`を使うため、`file:///C:/...`形式の`import.meta.url`を渡すと`file:\C:\...`という不正なURL文字列になり`fileURLToPath`が例外を投げる
- → 各ファイルに`export const runtime = 'edge'`を追加。Next.jsは`process.env.NEXT_RUNTIME === 'edge'`の場合`@vercel/og/index.edge.js`を使い、
  こちらはフォント/wasmを`fetch(new URL(...))`で読み込む実装のため`path.join`を経由せず問題が起きない
- 修正後`next build`は成功(`/icon`等は`ƒ (Dynamic)`としてビルドされる。「edge runtimeを使うとそのページの静的生成が無効になる」という警告が出るが、画像生成ルートは元々動的なので想定通り)
- 教訓: `next/og`の`ImageResponse`を使うルート(`icon.tsx`/`opengraph-image.tsx`等)は、Windows開発環境では**`export const runtime = 'edge'`を必ず付与する**。Mac/Linuxでは発生しない可能性があるが、Windows/Mac両対応(CLAUDE.md方針)のためビルド確認はWindows側で行う

**[方針確認] noindex/index方針: `/`はindex、`/share`・`/simulator`はnoindex(現状維持)**
- `/`(LP): 公開時の集客対象としてindex/follow(rootのグローバルnoindexバグ修正により実現)
- `/share`(共有ページ): ユーザー作成の共有レイアウトが検索結果に出ないようnoindex維持(変更なし)
- `/simulator`: 現状維持(noindex)を提案・docs/release-checklist.mdに記録。理由は①CSR中心でSSR/初期表示がほぼ空のプレースホルダ(クローラーから見て中身が薄い)、②LPとキーワードが重複しカニバリゼーションのリスクがあるため。公開後Search Consoleの実データを見てindex化を再検討する

**[実装] `/simulator`のフォールバック対象を576px(クラッシュ境界)→1024px未満(UX境界)に拡大**
- 前回の576pxクラッシュ修正は「壊れない」ための最小境界だったが、768〜1023px(縦向きタブレット等)は
  クラッシュこそしないものの3ペイン編集UI(左サイドバー320px+右パネル256px+中央canvas)が窮屈で実用に耐えない、
  というオーナーレビュー指摘を受け、安全側に倒してフォールバック対象を1024px未満まで拡大した
- `COMPACT_BREAKPOINT_QUERY = '(max-width: 1023px)'`に変更し、変数名も`isMobile`/`setIsMobile`/`MOBILE_BREAKPOINT_QUERY`から
  `isCompactViewport`/`setIsCompactViewport`/`COMPACT_BREAKPOINT_QUERY`にリネーム。1024px未満には縦向きタブレット
  (例: iPad縦=768px)が含まれ「モバイル」という呼称は実態と合わなくなったため
- フォールバック文言も「PC・タブレットでの編集に対応」→「PC・横向きタブレットでの編集に対応」、
  「スマートフォン向けの編集画面は準備中」→「スマートフォン・縦向きタブレット向けの編集画面は準備中」に調整し、
  対応端末の境界をユーザーに正確に伝えるようにした
- `mobile-fallback.spec.ts`は4件→7件に全面改訂し、390/575/768/1023px(フォールバック)・1024/1440px(通常)の
  6境界点をそれぞれ個別テスト化(+デスクトップ→モバイルリサイズの回帰テスト1件)。`simulator.spec.ts`(24件)は
  デフォルトviewport(1280×720、>1024px)を使うため無修正でpass継続を確認した
- 教訓: 「クラッシュしない最小境界」と「実用に耐える境界」は別物。クラッシュ修正後のレビューで「動くけど窮屈」
  という指摘が出たら、ブレークポイント自体を境界値ごと見直す(対症療法的なレイアウト微調整より、
  対象範囲を明確に区切るほうが小さい変更でリスクを下げられる場合がある)

### 2026-06-11（続き）

**[実装パターン] 法的ページ(`/terms`・`/privacy`)は共通レイアウト+Tailwind子要素セレクタで構成**
- `LegalPageLayout.tsx`を新設し、ヘッダー(ロゴ+トップへ戻る)・タイトル+最終更新日・本文(`children`)・末尾の相互リンク(利用規約⇄プライバシーポリシー⇄トップ)という骨格を共通化
- 本文側は`<section><h2>...</h2><p>...</p><ul><li>...</li></ul></section>`という素のJSXを書くだけで、親側の`[&_h2]:text-base [&_h2]:font-bold ... [&_p]:text-warm-gray [&_ul]:list-disc`のようなTailwind子孫セレクタでスタイルを一括適用する設計にした
- メリット: ページ側(`/terms/page.tsx`等)は文言(JSX)に専念でき、デザイン変更は`LegalPageLayout`1箇所の修正で全ページに反映される。法的文言は今後オーナー確認で頻繁に修正される想定のため、文言とスタイルの分離が特に有効

**[実装前チェック] フッター等の既存UIにリンク・文言を追加する前にE2Eテストへの依存をgrepで確認**
- `/`・`/simulator`・`/share`のフッターに`/terms`・`/privacy`へのリンクと免責一文を追加する前に、`apps/web/tests`配下で`© 2025|footer|利用規約|プライバシー|免責`等をgrepし、既存テストが現在のフッター文言・構造に依存していないことを確認してから着手した
- 結果、既存E2E(31件)に影響なくリンク追加でき、type-checkのみで安全性を確認できた
- 教訓: UIの末尾(フッター・補足文言)はE2Eの`toContainText`等で部分一致チェックされていることがあるため、追加前に軽くgrepしておくと「動いていたテストが文言追加で壊れる」事故を避けられる

**[方針] 運営者情報・連絡先・ドメインが未確定な法的ページは`【運営者名】`等のプレースホルダー+TODOコメントで先に構造を作る**
- リリース前チェックリストの「プライバシーポリシー→利用規約→免責文言→フッター導線→注意文言整理」という優先順位に対し、文面の最終確定(運営者名・連絡先・管轄裁判所・ドメイン)を待つとページ構成自体が一切進まなくなる
- → ページ構成・ルーティング(`/terms`・`/privacy`)・導線(各ページからのリンク)・文面のドラフトを先に全て作り、未確定箇所のみ`【運営者名】`等のプレースホルダー+ファイル冒頭のTODOコメント+`docs/release-checklist.md`への一覧化で「公開前に必ず確認すべき箇所」を可視化する、という進め方が有効だった
- 各ページの最終更新日も`2026-06-11（ドラフト・公開前にオーナー確認要）`という形で「ドラフトである」こと自体を明示しておくと、確認漏れのリスクが下がる

### 2026-06-11（続き2）

**[致命的バグ→修正] CSS Gridの子要素は既定`min-width: auto`のため、中身が大きいと`grid-cols-12`指定があってもグリッド全体がオーバーフローする**
- LP(`/`)のヒーローセクションは`grid lg:grid-cols-12`(モバイルでは`grid-cols`未指定=暗黙的に1カラムだが、Gridアイテム自体の`min-width`は`auto`のまま)で構成されており、390px viewportで`scrollWidth`が約1664pxになる横スクロールが発生していた
- 原因はGridアイテム(左の文言カラム・右の`HeroRoomPreview`カラム)の`min-width: auto`(Flexbox/Gridの初期値)により、内部コンテンツ(画像・固定幅要素等)の自然サイズがそのままアイテムの最小幅として扱われ、親Gridのトラック幅を超えて膨張していたこと
- → ①`grid lg:grid-cols-12`に明示的に`grid-cols-1`を追加(モバイルでは1カラムであることを明示) ②各Gridアイテム(`lg:col-span-6`の左右カラム)に`min-w-0`を追加し、`min-width: auto`を上書きしてコンテンツ側にオーバーフロー制御(折り返し・縮小)を委ねる、の2点で修正。修正後`scrollWidth === innerWidth === 390`を確認
- 教訓: モバイルで横スクロールが出る場合、`overflow-x-hidden`で隠す前に、Grid/Flexアイテムへの`min-w-0`(または`min-width: 0`)忘れを疑う。特に画像・固定幅子要素を含むカラムでは必須になりやすい

**[実装パターン] react-konvaで「親の回転に関わらず常に正立表示する子要素」は、子Groupに`rotation={-親のrotationDeg}`を付けて外接矩形(AABB)基準で配置する**
- `FurnitureObject2D.tsx`の寸法ラベル(`W×D`)は、家具本体のGroupが`rotation={instance.rotationDeg}`で回転すると一緒に回転・反転して読みにくくなっていた(180°回転時はラベルが上下逆になり、他の家具のラベルと重なることもあった)
- → ラベル用の子`<Group x={w/2} y={h/2} rotation={-instance.rotationDeg} listening={false}>`を追加。Konvaの変換合成は`親の変換 × 子の変換`なので、子に親と逆の回転を与えると子の見た目はワールド座標系で常に軸並行(正立)になる。位置は親のローカル座標系(回転後)の原点(`w/2, h/2`)を基準にしつつ、サイズは`Math.abs(w*cos)+Math.abs(h*sin)`等で計算した外接矩形(AABB)を使うことで、0°/90°/180°/270°いずれでも「回転後の見た目の下端中央」にラベルが来るようにした
- 0°回転時は`rotation={-0}=0`となり元のコードと数式上完全に一致することを確認してから適用。Konvaに限らずSVG/CSS Transformでも同じ「逆回転Group」パターンが使える
- 教訓: 「個々の要素は回転させたいが、ラベル・アイコン等の一部の子要素だけは画面に対して正立させたい」場合、子要素に親と逆方向の回転を与えるだけで実現できる。AABBの計算式(`|w*cosθ|+|h*sinθ|`, `|w*sinθ|+|h*cosθ|`)は回転矩形の外接箱を求める標準式として再利用できる

### 2026-06-11（続き3）

**[E2E失敗の罠] `playwright.config.ts`の`reuseExistingServer: !process.env.CI`は、前回セッションで起動したまま残っているdevサーバーを「正しいenvなし」で再利用してしまい、env依存のテストだけが失敗する**
- GA4実装後のE2E実行で、test 24「本番相当(URL自動取得無効)では「+URL」が準備中メッセージになり、手動入力は引き続き使える」のみが失敗(`url-import-disabled-message`が見つからない)
- 原因: `webServer.env`に`NEXT_PUBLIC_ENABLE_URL_IMPORT: 'false'`が設定されているが、ポート3000に前回タスク(スクリーンショット撮影)で起動したまま残っていた`next dev`プロセス(env設定なし=開発デフォルトでURL取り込み有効)をPlaywrightがそのまま再利用したため、このテストだけが意図通りの状態にならなかった
- → `netstat -ano`でポート3000のPIDを確認し`taskkill`で終了後に再実行したところ31/31 pass
- 教訓: GA4のようなenv var gated機能やE2E失敗の調査時、特定の1テストだけが失敗する場合は実装ミスを疑う前に「ポート3000に古いdevサーバーが残っていないか」を確認する。`pnpm dev`をバックグラウンドで起動したまま別タスクに移った場合は特に注意

---

## 合成ログ（週次レビュー時に記入）

*まだ合成なし — 2026-04-11 観察開始*

---

## 昇格済み（CLAUDE.md反映済み）

*まだなし*

---

*初版作成: 2026-04-11 | AI統括マネージャー*
