# Business-Tracker.md — 進捗・マイルストーン管理

> 「今何をやっているか」「次に何をやるか」を一元管理する生きた文書。
> 新しいアイデアを持ち込む前にこのファイルを確認し、既存の優先タスクと比較すること。
> 更新頻度: 作業のたびに随時。

---

## 現在のフェーズ

**Threads: フェーズ1 フォロワー獲得期**（2026-04〜収益化開始まで）
- 目標: 各アカウントで収益化ラインのフォロワー数を達成する
- 収益: 現在ゼロ（広告・提携収益はフォロワー数が基準を超えてから）

**KDP: フェーズ0 初期構築完了・初回実行待ち**（2026-04-12〜）
- 目標: 週1冊ペースで電子書籍を生成・出版する
- 収益: KDPアカウント開設後、初回出版から収益化開始

---

## 稼働中プロジェクト

### 01_Threads_Automation（メイン・唯一の稼働プロジェクト）

| ステータス | タスク | 期限 | 備考 |
|----------|------|------|------|
| ✅ 完了 | CLAUDE.md・ディレクトリ構造の整備 | 2026-04-10 | |
| ✅ 完了 | config.json のGit除外（セキュリティ） | 2026-04-10 | |
| ✅ 完了 | writer.py の trend_guide 全件適用 | 2026-04-11 | バズサーチデータを完全活用 |
| ✅ 完了 | bypassPermissions 設定 | 2026-04-11 | 毎回の許可確認を解消 |
| 🔄 進行中 | フォロワー獲得・投稿継続 | 継続中 | 4アカウント稼働中 |
| ⚠️ 未対応 | token_manager の無人実行対応 | 期限: 2026-05-12頃 | App Secretの安全な保存方法が必要。トークン期限7日前に対処が必要 |
| ✅ 完了 | Meta for Developers 再登録 | 2026-04-14 | 新アプリID: 1422148273258080。C/D/E/Hのトークン再発行済み |
| ⚠️ 審査待ち | れな アカウントのトークン再発行 | 審査完了後 | Meta審査中のため一時保留。審査通過後に新アプリで短期トークンを発行し、config.jsonに追加すること |
| ⬜ 未着手 | ログ監視・異常検知の仕組み | 未定 | launchd実行の成否が現状把握できない |
| ⬜ 未着手 | 月次KPIの実績記録開始 | 2026-05-01 | フォロワー数・投稿数・APIコストを記録 |

---

### 04_KDP_Automation（稼働中・初回出版申請済み）

| ステータス | タスク | 期限 | 備考 |
|----------|------|------|------|
| ✅ 完了 | パイプライン初期構築 | 2026-04-12 | researcher/scorer/writer/formatter/main |
| ✅ 完了 | KDPアカウント開設・税務情報登録 | 2026-04-12 | W-8BEN署名済み |
| ✅ 完了 | 初回出版申請（ChatGPT・Claude完全攻略ガイド） | 2026-04-12 | ¥980・審査中（72時間以内に販売開始） |
| ✅ 完了 | launchd 週次スケジュール登録（毎週日曜23:00） | 2026-04-12 | mac_setup.shに組み込み済み |
| ✅ 完了 | fal.ai表紙自動生成・transfer_to_windows.sh・record_asin.py 実装 | 2026-04-12 | |
| ✅ 完了 | Mac側で git pull して最新コードを反映 | 2026-04-12 | fal.ai表紙生成・KDP_upload_info.md自動生成を有効化 |
| ✅ 完了 | ASIN記録（販売開始後） | 2026-04-15 | ASIN: B0GX2VQJPC。`python3 record_asin.py B0GX2VQJPC` をMacで実行すること |
| ✅ 完了 | KDPセレクト登録 | 2026-04-15 | Kindle Unlimited 対象・KENP収益発生開始 |
| ✅ 完了 | 著者セントラル登録 | 2026-04-15 | 著者ページ公開済み・本の紐付け完了 |
| ⬜ 未着手 | Amazon広告（AMS）開始 | 任意 | オート＋マニュアル併用。初期予算¥500/日 |
| ✅ 完了 | 40代からの資産形成戦略 の出版判断 | 2026-04-12 | 出版しない決定。book_history.json: cancelled |
| ⬜ 未着手 | 第2回出版（次の日曜自動生成分） | 2026-04-19 | Macで自動実行予定 |

---

### 02_Project_Incubator / おけるかな（家具配置シミュレーター、MVP開発中）

| ステータス | タスク | 期限 | 備考 |
|----------|------|------|------|
| ✅ 完了 | Day1〜7 MVP実装（手動入力・2Dエディタ・保存・買い物リスト） | 2026-06 | |
| ✅ 完了 | Playwright E2E テスト 10/10 全通過 | 2026-06 | |
| ✅ 完了 | KeepaProvider・MockProvider 実装（切替方式） | 2026-06 | |
| ✅ 完了 | GitHub remoteリポジトリ作成・push | 2026-06-09 | https://github.com/noregista/furniture-layout-simulator (private) |
| ✅ 完了 | Priority-A UI改善: インテリアデザイン感強化 | 2026-06-10 | 家具ビジュアル・サンプル6点・ShoppingList・ヒーロー刷新。E2E 13/13 pass |
| ✅ 完了 | Priority-A追加: 家具リアリティ・キャンバス質感向上 | 2026-06-10 | bed/desk/chair/rug等の家具マーカー全面刷新、選択枠を上品に、壁・グリッド・床をsofterに、サンプルレイアウト再構成、ヒーロー差し替え。E2E 13/13 pass |
| ✅ 完了 | 家具表現の根本刷新（専用アイコン化）+ LP全面リデザイン | 2026-06-10 | 優先6カテゴリ(bed/desk/chair/rug/tv_stand/storage_shelf)を専用Konvaコンポーネント化。Warm Editorialパレット導入。LPヒーローを「部屋イラスト＋失敗回避コピー」に全面刷新（旧モックアップ廃止）。リファクタ起因の重大バグ（優先6カテゴリの家具がキャンバス上でクリック選択・ドラッグ不能）を発見・修正。E2E 13/13 pass |
| ✅ 完了 | 見た目の質感・プロダクト感の微調整（共有URL前の最終仕上げ） | 2026-06-10 | オーナーレビュー指摘5点に対応：①チェアを記号的D字型から自然なデスクチェア形状に再設計 ②ラグの赤枠を縮小・減色して主張を抑制 ③素材パレットをウォルナット/チャコール寄りに調整し締まりを付与 ④LPヒーローを6:6カラム化＋bleed余白で拡大強化 ⑤「部屋に置く」ボタンを通常時控えめ・hover/選択時に主ボタン化。スクリーンショット01-09再取得。E2E 13/13 pass |
| ✅ 完了 | 匿名共有URL機能 | 2026-06-10 | `/share#data=<圧縮データ>`方式（hash fragment・サーバー保存なし）。URL長上限2000・items50件上限・個人情報非含有・decode失敗時は専用エラー画面。リミックス（自分の部屋として開く＝上書き）対応。E2E 15/15 pass |
| ✅ 完了 | 簡易3Dプレビュー | 2026-06-11 | @react-three/fiber+drei。箱型家具+床+壁2面+OrbitControls。2D/3Dトグル実装、2D編集体験は維持。/share再利用可能な汎用設計。E2E 17/17 pass |
| ✅ 完了 | リリース前最終棚卸し（docs/release-checklist.md作成） | 2026-06-11 | Keepa未導入時のコピー修正(Amazon URL自動取得を言い切らない)、3D表記を「簡易3D」に統一、共有ポップオーバーに注意書き2点追加(レイアウト情報含有/個人情報禁止)、GA4イベント設計案(8件)・公開前QAリスト(10件)・Keepa検証準備状況を整理。型チェック・E2E 17/17 pass |
| ✅ 完了 | リリース前自動検証スクリプト(self-check-release-readiness.ts)実装 | 2026-06-12 | LP/Simulator/Share/Terms/Privacyの全5領域を本番相当設定(`NEXT_PUBLIC_ENABLE_URL_IMPORT=false`)で自動巡回し、PASS/FAIL/INFOレポート(`screenshots/release_readiness/README.md`)+スクリーンショット12枚を自動生成。`pnpm run self-check:release`で公開直前に毎回実行可能。初回実行34/34 PASS(INFO2件=プレースホルダー検出のみ・想定どおり)。type-check・E2E 31/31 pass。docs/release-checklist.mdセクション12に追記 |
| ✅ 完了 | 公開前preflightコマンド(pnpm run preflight)実装 | 2026-06-12 | type-check → production build(apps/web) → E2E全件(31件) → release readiness self-checkを1コマンドで一括実行(`scripts/preflight.ts`)。失敗時は以降をスキップしPASS/FAIL/SKIPサマリ＋レポート保存先(`furniture-layout-simulator/screenshots/release_readiness/README.md`)を表示。初回実行は全PASS(type-check/build/E2E 31-31/self-check 34 PASS・0 FAIL・2 INFO)。**公開判断時はこれを実行する運用**。docs/release-checklist.mdセクション13に追記。commit: dbaa556・push済み |
| ✅ 確定(2026-06-13) | **Keepa API検証の位置づけ確定（案A: 公開前必須）** | 公開判断の前提 | オーナーより**案A「公開前必須」を維持**することが確定（案B「URL自動取得機能のリリース前必須へ格下げ・手動入力版での先行公開」は不採用）。URL自動取得なしでは正式公開しない方針。Keepa課金は実施予定で、実API検証してからデプロイ判断する。下記3行（Keepa API検証/採用判定/MockProviderフォールバック方針）はすべて公開前必須タスクとして維持。詳細は`docs/release-checklist.md`セクション7・14、`docs/owner-decision-pack.md`セクション0・2参照 |
| ⬜ 未実施(公開前必須・確定) | **Keepa API検証**（Amazon.co.jp 家具40件/10カテゴリ） | 公開前必須 | 検証スクリプト・対象リスト・結果フォーマット(JSON/CSV/MD)・判定基準は整備済み(2026-06-12)。`verify-keepa`は`not_run`(`KEEPA_API_KEY`未設定時・デフォルト=実APIを呼ばず安全終了)/`demo`(`--demo`、`source: mock_demo`・本番採用判断には使用不可)/`real`(キー設定時)の3モード。実行順序: ①`scripts/fixtures/keepa-targets.json`のASIN実在確認 → ②Keepa課金(オーナー操作待ち) → ③`KEEPA_API_KEY`設定 → ④`pnpm --filter @fls/scripts verify-keepa`実行 → ⑤結果に基づきデプロイ判断。詳細: `docs/keepa-verification-targets.md` |
| ⬜ 未実施(公開前必須・確定) | Keepa採用判定・KeepaProvider 本番切替 | 公開前必須 | 検証結果に基づき判定。寸法が取れなくても商品名+画像URLだけで価値あり → 手動修正UIにフォールバック |
| ⬜ 未実施(公開前必須・確定) | MockProviderのモック商品フォールバック方針の対応 | 公開前必須 | KEEPA_API_KEY未設定時、実URLでも「モック商品(ASIN)」+疑似乱数寸法が「要確認」バッジのみで配置可能になる問題。案A確定により公開前に対応が必要。release-checklist.md参照 |
| ✅ 完了 | favicon・app icon・OGP/Twitter Card・metadataBase・noindex/index整理 | 2026-06-11 | `next/og`で動的生成(favicon32×32・apple-icon180×180・OGP/Twitter1200×630、Warm Editorialパレットの図形のみ)。`metadataBase`は`NEXT_PUBLIC_SITE_URL`環境変数化(未設定時localhost)。rootのグローバルnoindexバグを修正し`/`をindex化、`/share`・`/simulator`はnoindex維持 |
| ✅ 完了(確定情報反映済み2026-06-13) | 利用規約・プライバシーポリシー・免責文言ページ | リリース前にオーナー最終確認 | `/terms`・`/privacy`を新設、LP/`/simulator`/`/share`に導線・免責一文を追加。運営者名(saison)・問い合わせ先(okerukana@gmail.com)・管轄裁判所(大阪地方裁判所)・サービス名(おけるかな)を反映済み(プレースホルダー解消)。release-checklist.md セクション10参照 |
| ✅ 完了(本番有効化方針確定2026-06-13) | GA4導入（8イベント計測基盤） | 2026-06-11 | `NEXT_PUBLIC_GA_MEASUREMENT_ID`未設定時はスクリプト未読込・無効。設計8イベント実装済み・type-check pass・E2E 31/31 pass。**本番で有効化する方針が確定**し、`/privacy`セクション2・4にGA4利用に関する記載を反映済み(release-checklist.md セクション5参照)。実測定ID設定は未実施 |
| ✅ 完了 | 「人のスケール」機能（複数人・姿勢対応） | 2026-06-11 | 最大4人、立つ/座る/寝るの3姿勢に対応した実用機能として実装。オーナーレビュー後のフィードバック4点(standing床基準化・共有エラー文言・2D視認性・3D見た目)対応も完了。詳細は直近の完了事項を参照 |
| ✅ 完了 | `/simulator` モバイル幅クラッシュ修正・本番公開前安全化 | 2026-06-11 | 576px境界(左サイドバー320px+右パネル256px)でcanvas-areaが0になりreact-konvaがdrawImageでクラッシュする致命的バグを修正。768px未満はPC/タブレット推奨フォールバック画面を表示し編集UI(2D/3D Canvas)を一切マウントしない方式に変更。RoomCanvas2D/Room3DSceneにcanvasサイズ0時の非描画ガードも追加(防御的)。MockProviderの本番安全化(「+URL」を準備中表示に)も実施。E2E 28/28・type-check pass。詳細は直近の完了事項を参照 |
| ✅ 完了 | `/simulator` 768px(タブレット縦)でのUI窮屈さ改善 | 2026-06-11 | 改善候補①(フォールバック対象を1024px未満に拡大)を採用。768〜1023pxは通常編集UIではなくPC・横向きタブレット推奨フォールバックを表示するよう変更。E2E 31/31・type-check pass。改善候補②(左/右パネルのDrawer化)は引き続き任意・未着手として残す |
| ⬜ 未着手 | `/simulator` 左/右パネルのDrawer化(開閉式)検討 | 任意 | 1024px未満フォールバック拡大により当面の窮屈さ問題は解消。将来的にスマホ・縦向きタブレット編集対応を行う場合の設計候補として残す |
| ✅ 完了 | UI/UXポリッシュ(公開前最終調整、A1-A4・B5-B10の10項目) | 2026-06-11 | 必須4項目: LPモバイル横オーバーフロー修正・3D人物standingの太さ調整・2D回転家具ラベル常時正立化・モバイルフォールバック見出し改行修正。任意6項目: 右パネル空状態改善・人のスケールカードのボタン強弱調整・3D壁色warm化・共有ページ見出し/CTA文言改善・商品カードCTA視認性向上。type-check pass・E2E 31/31 pass・Before/Afterスクリーンショット確認済み。詳細は`docs/release-checklist.md`セクション11参照 |
| ✅ 完了 | UI/UXポリッシュ第2弾(優先度A全8項目: 採寸図感の解消) | 2026-06-12 | オーナーレビュー指摘「採寸ツール感・AIテンプレ感・開発中ツール感」への対応。①寸法ラベルを選択中のみ表示(常時非表示化) ②人物アイコンをグレージュ/テラコッタ系に配色変更+頭部比率縮小 ③3D家具に面別簡易シェーディング追加(shadeColorユーティリティ新規) ④共有ページのタイトル/説明文を「誰かが考えたお部屋のレイアウト」に変更・部屋サイズをキャプション化 ⑤価格未設定の黄色警告バナーを廃止・買い物リストに「価格を追加」インライン入力導線を追加 ⑥LPヒーローをアプリ画面風からレイアウトカード+キャプションに変更 ⑦「人のスケール」カードを家具リストの下へ移動・優先度低下 ⑧右パネル空状態を「次にできること」3カードガイドに変更。type-check・E2E 31/31・preflight(34 PASS/0 FAIL/2 INFO)すべてPASS。スクリーンショット10枚を`screenshots/ui_priority_a_after/`に保存(撮影スクリプト: `scripts/self-check-ui-priority-a-after.ts`)。commit: c6243e7（push未実施・オーナー確認待ち） |
| ✅ 完了 | B2: 人物の初期配置・重なり順改善(低リスク範囲) | 2026-06-12 | `findFreeStandingPositionCm`を中心点判定からフットプリントAABB×家具/人物AABBの矩形重なり判定に変更(`getRotatedAABB`/`aabbOverlap`/`overlapsAnyRect`新設)。`addPerson`をフットプリント+10cmギャップ基準のグリッド探索に変更し4人配置時の重なりを解消。`clampFootprintToRoomCm`新設でpose変更後のフットプリントを部屋内にクランプ。選択中人物のみ描画順を最前面に回す`renderedPeople`導入(データ順序は不変)。共有ページの人物本体opacity 0.85〜0.95に向上・身長ラベルは控えめ表示(家具寸法ラベルは復活させず)。type-check・E2E 31/31・preflight(34 PASS/0 FAIL/2 INFO)全PASS。screenshots/people_b2_after/に7枚保存。commit: c71ba81・push済み |
| ✅ 完了 | B1: 2D家具アイコンの質感改善(sofa/bookcase/table・任意でlighting) | 2026-06-12 | `SofaIcon.tsx`/`BookcaseIcon.tsx`/`TableIcon.tsx`/`LightingIcon.tsx`を新規実装し`FURNITURE_ICONS`に登録。ソファは背もたれ+左右肘掛け+座面クッション3分割(折りジワ)、本棚は棚板フレーム+縦仕切り3区画+高さ違いの本の背表紙、テーブルは木目天板+縁ベベル+四隅の控えめな脚ヒントで表現。type-check・E2E 31/31・preflight(34 PASS/0 FAIL/2 INFO)全PASS。8種のBefore/Afterスクリーンショットでオーナーレビュー合格。commit: a9fabb2・push済み。残課題(任意・公開ブロッカーではない): ソファの色が冷たいグレー寄り、テーブルが若干平面的、チェアのロボット感→優先度B/Cバックログに記録 |
| ✅ 完了 | B3: LPの独自性改善（「SaaSっぽい機能紹介」→「買う前に確認する生活者向け体験」） | 2026-06-13 | LP全体の主語を「ツール」から「買う前の不安」へ寄せる方針で7項目を実装。①ヒーロー: 「家具配置シミュレーター」バッジ追加+通路幅/余白訴求のサブコピー+Nav/CTAを「置いてみる」系に統一+ヒーロープレビューキャプション変更 ②CTA文言統一(「サンプル部屋に置いてみる」「自分の部屋で置いてみる」「6畳ワンルームで試してみる」、「試す」連発回避) ③3ステップを生活者視点に書き換え(「家具のサイズを控える」「部屋に置いて動かす」「余白と動線を確認する」、Amazon URL・自動取得言及を削除) ④課題セクション4カードにアイコン背景色/アクセントカラー追加 ⑤ダークセクションを「安心して使える理由」に再構成(bg-wood-dark新色、登録なし/ブラウザ保存/画像非保存/共有URL限定公開を訴求) ⑥下部CTAを操作説明からベネフィット視点に変更 ⑦モバイル(390px)レビューで見出し改行2件を修正。type-check pass・E2E 31/31 pass・preflight(34 PASS/0 FAIL/2 INFO)全PASS。スクリーンショット9枚を`screenshots/b3_lp_after/`に保存(Before:`b3_lp_before/`)。commit: 23e6186・push済み(origin/mainと同期確認済み) |
| ✅ 方針確定(初期非導入) | 収益化方法検討（広告・月額・アフィリエイト） | リリース後に再検討 | 2026-06-13オーナー確定: 初期公開時は広告・アフィリエイト(Amazonアソシエイト含む)を一切導入しない。まず「おけるかな」のビュー数・利用状況・共有数を確認し、伸びてきた段階で再検討する。Amazonアソシエイト・広告掲載は将来の収益化候補として下記アイデアバックログに残す。LP・シミュレーター・共有ページへの広告枠・アフィリエイト導線追加は現時点では行わない(コード変更なし)。詳細は`furniture-layout-simulator/docs/owner-decision-pack.md`セクション9参照 |

---

#### UI/デザイン改善バックログ（優先度B/C・公開後改善候補）— 2026-06-12整理

> 優先度A全8項目(2026-06-12 push済み、commit c6243e7)で「採寸図感の解消」は完了。オーナーレビューで挙げられた残課題8件を、次フェーズ候補として優先度B/Cで整理する。**いずれも公開ブロッカーではなく、公開後改善でよい項目**。公開ブロッカー・オーナー判断事項との切り分けは`docs/release-checklist.md`セクション14「公開判断マトリクス」参照。

**B1. 2D家具アイコンの質感改善** — ✅ 完了(2026-06-12)
- 優先度: B
- 目的: 「整理されたアイコン感」を脱し、各家具がより「本物の家具らしい」質感・素材感を持つようにする
- 現状の問題: 専用Konvaアイコン化(2026-06-10)で記号感は改善したが、依然フラットな色面+線のみの構成で、木目・布地・金属等の質感表現がない
- 実装方針: 既存の各家具コンポーネント(BedIcon2D等)にKonva LinearGradient・微細パターン・縁取りのコントラスト強化などを段階的に追加。形状の大規模変更や新規アイコン追加はしない(今回の3D面別シェーディングと同じ「マテリアル調整」アプローチ)
- 今すぐやらない理由(着手前メモ): 機能追加ではない見た目の質感調整であり、各家具ごとに個別レビューが必要で時間がかかる。公開ブロッカーより優先度が低い
- 着手タイミング(着手前メモ): 公開後、最初のユーザーフィードバックを得てから。時間があれば優先6カテゴリのうち最も目立つ1-2点(ベッド・デスク等)から試験着手も可
- ✅完了報告: sofa/bookcase/table(・任意でlighting)の4カテゴリに新規Konvaアイコン(`SofaIcon`/`BookcaseIcon`/`TableIcon`/`LightingIcon`)を実装し`FURNITURE_ICONS`に登録。ソファ=背もたれ+左右肘掛け+座面クッション3分割(折りジワ)、本棚=棚板フレーム+縦仕切り3区画+高さ違いの本の背表紙+足元影、テーブル=木目天板+縁ベベル+四隅の控えめな脚ヒントで「濃い長方形」「ボタン付きの板」感を解消。type-check・E2E 31/31・preflight(34 PASS/0 FAIL/2 INFO)全PASS。10カテゴリ一覧・Before/After・共有ページ・90度回転の8種スクリーンショットでオーナーレビュー実施、合格。commit: a9fabb2・push済み。残課題(将来の任意改善・公開ブロッカーではない): ソファの色がやや冷たいグレー寄り、テーブルがまだ若干平面的、チェアのロボット感。次フェーズ候補としてこのバックログに残す

**B2. 人物の初期配置・重なり順改善** — ✅ 完了(2026-06-12)
- 優先度: B
- 目的: 2D/3D/共有ページで複数人を配置した際に人物が家具や他の人物と重なって視認性が落ちる問題を解消し、「人のスケール」機能の実用性を高める
- 現状の問題: 今回のスクリーンショット(05/06/08)で2人目以降の人物が家具・他の人物に隠れて見えにくいケースを確認。`addPerson`の初期配置(`findFreeStandingPositionCm`)は家具との重なり回避のみで、人物同士の重なりや描画順(z-order)は未対応
- 実装方針: ①`addPerson`の初期位置決定で既存人物群とのAABB重複も回避対象に追加 ②2D描画順を「人物は常に家具より前面」または「選択中の人物を最前面」に固定するルールを実装 ③共有ページ(RoomViewer)にも同じ描画順を適用
- 今すぐやらない理由(着手前メモ): 今回の目的(採寸図感の解消)とは直接関係しない実用面の改善で、クリック選択すれば現状でも個別確認は可能。配置ロジック変更はE2E影響範囲調査が必要で工数がかかる
- 着手タイミング(着手前メモ): 公開後、複数人配置の利用が増えた段階。または次回UIポリッシュ枠でE2E影響調査とセットで着手
- ✅完了報告: オーナー指示により低リスク範囲(上記実装方針①②③+pose変更時の部屋内クランプ)で実装完了。type-check・E2E 31/31・preflight全PASS。commit: c71ba81・push済み。詳細は「直近の完了事項」・LEARNINGS.md 2026-06-12参照。pose変更時の家具・他人物との自動重なり回避は今回スコープ外

**B3. LPの独自性改善** — ✅ 完了(2026-06-13)
- 優先度: B
- 目的: 「その家具、部屋に置いたらどうなる？」訴求を維持しつつ、LP全体のビジュアル構成・配色・タイポグラフィに独自性を持たせ、SaaSテンプレ感を脱する
- 現状の問題: Warm Editorialパレット導入・ヒーローのカード化で改善は進んだが、セクション構成(ヒーロー→特徴3点→ステップ→CTA)や角丸カード+アイコンの並びは一般的なSaaS LPパターンに近く、イラスト・タイポグラフィ等の個性が弱い
- 実装方針: ①ヒーロー以外のセクションにも部屋イラスト/アイコンを活用しテキストのみのカードを減らす ②見出しフォント・余白・セクション区切りの装飾でブランドらしさを追加。既存セクション構成を維持した上での装飾・素材追加に限定し大規模リデザインはしない
- 今すぐやらない理由(着手前メモ): 「独自性」は主観的判断要素が大きく、方向性についてオーナーの好み・ブランドイメージ確認がコード変更前に必要。ドキュメント整理フェーズでは着手しない
- 着手タイミング(着手前メモ): 公開後、もしくは公開前でもオーナーとデザイン方向性(イラスト追加可否・トンマナ)を確認できたタイミング
- ✅完了報告: オーナー指示により、方向性を「ビジュアル装飾の独自性」から「LPの主語をツールから『買う前の不安』に寄せる」というコピー・構成の独自性に再定義して実装。大規模リデザインはせず既存構成のポリッシュに留めた。ヒーローバッジ・CTA文言統一・3ステップ書き換え・課題セクションのアクセントカラー・ダークセクション再構成(「安心して使える理由」)・下部CTAのベネフィット化・モバイル見出し改行修正の7項目+2件の改行調整を実施。type-check・E2E 31/31・preflight(34 PASS/0 FAIL/2 INFO)全PASS。commit: 23e6186・push済み。詳細はLEARNINGS.md 2026-06-13参照

**C1. 3D家具表現の改善**
- 優先度: C
- 目的: 簡易3Dの「箱感」をさらに軽減し、家具カテゴリごとの形状的特徴(脚・背もたれ等)がうっすら分かるようにする
- 現状の問題: 面別シェーディング(今回実装)で立体感は向上したが、全カテゴリ共通のBoxGeometryのため、ベッド・デスク・チェア等の形状差は3Dで表現されない
- 実装方針: 一部カテゴリ(chair, tv_stand等)に限り、複数BoxGeometryの組み合わせによる簡易複合形状(脚+座面+背もたれ等)を追加。GLTF等の外部3Dモデル導入は行わない
- 今すぐやらない理由: release-checklist.mdの方針「現状の3Dは『売りになる高品質3D』ではなく『高さ感を確認する簡易プレビュー』」を維持する以上ROIが低く、公開ブロッカーより明確に優先度が低い
- 着手タイミング: 公開後、3D機能の利用率・フィードバックを見てから。「簡易3D」の位置づけ自体を見直す場合のみ着手

**C2. 共有ページの見せ方改善**
- 優先度: C
- 目的: 今回改善した文言・価格表示に続き、レイアウトプレビューの見せ方(余白・カード構成・CTA導線)を磨き、リミックスへの誘導力を高める
- 現状の問題: 文言・価格表示は改善済みだが、レイアウト全体の構成(プレビュー→家具リスト→CTA)は初回実装時のまま。プレビューの余白バランスやCTAボタン配置に改善余地が残る
- 実装方針: `ShareView.tsx`の余白・カード境界線・CTAボタン配置の微調整(構造変更なし)。プレビューとインテリアリストの視覚的な繋がり(角丸・背景トーンの統一)を強化
- 今すぐやらない理由: 今回(優先度A)で「内容面」(文言・価格表示)の改善は完了済み。レイアウト微調整の影響は小さく、他の高ROI項目(LP独自性・2D家具質感)を優先すべき
- 着手タイミング: 公開後、共有URL機能の利用状況(共有数・リミックス率)を見てから優先度を再評価

**C3. モバイルフォールバック文言/見せ方の追加改善**
- 優先度: C
- 目的: 1024px未満で表示される「PC・横向きタブレット推奨」フォールバック画面の文言・デザインを、サービス全体のトンマナに近づける
- 現状の問題: 現状はテキスト中心の案内画面(見出し+説明+トップへ戻るボタン)で、LP・シミュレーターと比べてデザインの統一感が薄い。モバイルでも閲覧可能な`/share`への導線もない
- 実装方針: フォールバック画面にWarm Editorialパレットの背景・簡易イラストを追加してLPと一貫したトンマナにする。「共有ページのサンプルを見る」等、`/share`への導線リンク追加を検討
- 今すぐやらない理由: 1024px未満は編集機能を提供しない画面で、公開直後のコンバージョンへの影響は限定的。他のB項目より優先度が低い
- 着手タイミング: 公開後、モバイル経由のアクセス比率・離脱率データを見てから

**C4. インテリアリストの価格表示まわりの改善**
- 優先度: C
- 目的: 今回追加した「価格を追加」インライン入力導線を、入力後の再編集・削除・一括設定まで含めて使いやすくする
- 現状の問題: 現状は「価格を追加」→数値入力→Enter/blurで確定のみ。入力済み価格の再編集・削除(未設定に戻す)導線がなく、合計欄の補足注記の位置にも改善余地がある
- 実装方針: 価格表示済みの行にも編集導線(クリックで`editingProductId`をセットし既存値を初期表示)・削除ボタンを追加。`updateProduct`での価格削除(`price: undefined`)許容を検討
- 今すぐやらない理由: 今回の優先度A対応で「価格未設定表示の弱体化+追加導線」という主目的は達成済み。編集・削除機能は使い込まれてから需要が見えるため現時点では優先度が低い
- 着手タイミング: 公開後、ユーザーが実際に価格入力を使い始め、編集・削除の要望が出た場合

**C5. 3Dの壁・床・ラグの質感改善**
- 優先度: C
- 目的: 簡易3Dの壁・床・ラグ(平面オブジェクト)に、現状の単色塗りより質感のあるマテリアル表現を加える
- 現状の問題: B7(2026-06-11)でライティングを暖色化したが、壁・床・ラグは単色`meshStandardMaterial`のままで、今回の3D家具シェーディングとの質感差が大きい
- 実装方針: 壁・床にFurnitureBox3Dと同様の面別シェーディング(`shadeColor`再利用)を適用し、ラグは既存2D色をベースに`roughness`/`metalness`を微調整。テクスチャ画像・外部アセットは導入しない
- 今すぐやらない理由: C1(3D家具表現の改善)と同じ理由でROIが低く、「簡易3D」の位置づけを維持する限り単独着手の優先度は低い
- 着手タイミング: C1着手時に合わせて検討。単独では着手しない

---

## 停止中プロジェクト（再開待ち）

| プロジェクト | 停止理由 | 再開条件 |
|------------|---------|---------|
| ゲームニュース（account_a/b） | 意図的停止 | オーナー判断 |
| 動画パイプライン（account_f/g） | 動画生成未稼働 | fal.ai 連携再構築後 |

---

## アイデアバックログ

> 新しいアイデアはここに貯める。既存のマイルストーンが完了してから着手を判断する。

| アイデア | 登録日 | ROI見込み | 着手可能条件 |
|---------|------|----------|------------|
| 動画パイプライン再開 | 2026-04-11 | 中 | フォロワー基盤が安定してから |
| Brain × KDP二次展開 | 2026-04-12 | 高 | KDP初回審査通過後。同コンテンツを300〜500円でBrain出品。アフィリエイター拡散で追加収益。追加執筆コストゼロ |
| X Revenue Sharing参入 | 2026-04-12 | 高 | オーナー判断待ち。今がボーナスタイムとの情報あり |
| 「おけるかな」広告/Amazonアソシエイト導入 | 2026-06-13 | 未評価 | 初期公開時は導入しない方針(2026-06-13確定)。ビュー数・利用数・共有数が伸びてきた段階で再検討 |

---

## 直近の完了事項（直近30日）

- 2026-06-13: 確定事項（サービス名・運営者情報・ドメイン/デプロイ・GA4・Keepa位置づけ）のサイト/規約/ドキュメントへの反映完了 — オーナーより以下が確定し反映した。①サービス名「おけるかな」（運営者名saison・問い合わせ先okerukana@gmail.com・管轄裁判所大阪地方裁判所）②正式ドメイン`okerukana.com`（お名前.comで取得予定）③デプロイ先AWS（Amplify Hosting + Lambda/API Gateway）④GA4は本番で有効化する⑤Keepaは案A「公開前必須」を維持（案B不採用、URL自動取得なしでは正式公開しない）⑥広告/アフィリエイトは初期非導入を維持（変更なし）。サイト本体は`apps/web/src/app/layout.tsx`(SITE_NAME)・LP(`page.tsx`)フッター・`/terms`・`/privacy`・`/share`・`/simulator`・`LegalPageLayout.tsx`・`ShareView.tsx`・`SimulatorLayout.tsx`・`ShoppingList.tsx`・`README.md`の表記を「おけるかな」に統一(自然な説明文の「家具配置シミュレーター」は維持)。`/terms`は`【正式サービス名】`等のプレースホルダーを全て確定情報に置換(法務文言の大幅リライトはせず構造を維持)。`/privacy`は同様に置換のうえ、「アクセス解析ツール等は導入していません」をGA4利用前提の記載(Cookie利用・個人非特定・ブラウザでの無効化可・Googleポリシー参照)に更新。`.env.example`にドメイン/GA4設定に関する注記を追加(実値設定はせず)。`docs/release-checklist.md`・`docs/owner-decision-pack.md`・`scripts/self-check-release-readiness.ts`の案A/案B記述・残課題リストを確定内容に更新。今回はドメイン取得・AWSデプロイ・GA4実測定ID設定・Keepa課金・KEEPA_API_KEY設定・実Keepa API呼び出し・広告タグ追加・Amazonアソシエイト導入は一切実施せず、反映・整理のみ。検証結果: `pnpm run preflight`実行で type-check PASS(4パッケージ)・production build PASS(8/8静的ページ)・E2E 31/31 PASS・release readiness self-check **36 PASS/0 FAIL/0 INFO**(従来の`/terms`・`/privacy`プレースホルダーINFO2件は解消)。スクリーンショット12枚を`screenshots/release_readiness/`に再取得。なお検証中、プロジェクトディレクトリ移動(`/c/dev/furniture-layout-simulator` → `/c/dev/services/furniture-layout-simulator`)に伴い`scripts/node_modules`内のシンボリックリンクが旧パスを指したまま残っており`playwright`モジュール解決に失敗する問題を発見。`scripts`を`pnpm-workspace.yaml`に追加・`scripts/package.json`に`playwright`を直接依存として追加し`pnpm install`で解消(`pnpm-lock.yaml`更新、サイトのコード・コンテンツへの影響なし)
- 2026-06-13: 「おけるかな」広告/アフィリエイト方針確定(ドキュメント記録のみ・コード変更なし) — オーナーより「初期公開時は広告・アフィリエイトを入れない(Amazonアソシエイトも初期導入なし)。まずビュー数・利用状況・共有数を確認し、伸びてきた段階で再検討する。将来的な収益化候補としてバックログに残す」との方針が確定。本ファイル(上記「収益化方法検討」行・アイデアバックログ)・`furniture-layout-simulator/docs/owner-decision-pack.md`(現在の状態まとめ・オーナー回答欄No.10・新設セクション9)・`furniture-layout-simulator/docs/release-checklist.md`(セクション13)・LEARNINGS.mdに記録。広告タグ追加・Amazonアソシエイト申請/導入・UIへの広告枠追加は一切実施せず、01_Threads_Automationにも変更なし
- 2026-06-13: B3「LPの独自性改善」実装完了(優先度B/Cバックログより着手) — オーナー指示に基づき、LP刷新の方向性を「ビジュアル装飾の独自性」から「LP全体を『SaaSっぽい機能紹介』から『家具を買う前の失敗を防ぐ生活者向けの体験』に寄せる」というコピー・構成面の独自性に再定義し実装。主語を「ツール」から「買う前の不安」へ、「試す」より「置いてみる/買う前に確認する」を優先する方針で7項目を実装: ①ヒーローに「家具配置シミュレーター」バッジ追加+通路幅/余白訴求のサブコピー+CTA「置いてみる」化+ヒーロープレビューキャプション変更 ②CTA文言統一(「サンプル部屋に置いてみる」「自分の部屋で置いてみる」「6畳ワンルームで試してみる」) ③3ステップを「家具のサイズを控える/部屋に置いて動かす/余白と動線を確認する」に書き換え、Amazon URL・将来自動取得言及を削除 ④課題セクション4カードにアイコン背景色・アクセントカラー(slate-blue/terracotta/sage/honey系)を追加 ⑤旧Feature Highlightsを「安心して使える理由」に再構成、背景をbg-ink→bg-wood-dark(新色#5E4530)に変更し登録なし/ブラウザ保存/画像非保存/共有URL限定公開を訴求 ⑥下部CTAを「6点配置される」操作説明からベネフィット視点(余白・動線確認)に変更 ⑦モバイル(390px)レビューで発見した見出し改行2件(下部CTA・3ステップ見出し)を修正。type-check pass・E2E 31/31 pass・preflight(34 PASS/0 FAIL/2 INFO)全PASS。スクリーンショット9枚を`screenshots/b3_lp_after/`に保存(Before:`b3_lp_before/`、撮影スクリプト: `scripts/self-check-lp-b3-after.ts`/`-before.ts`)。残課題: release readinessのINFO2件(`/terms`・`/privacy`のプレースホルダー文言)はB3スコープ外で別タスクとして継続。Keepa API本検証は引き続きリリース前必須タスク。commit: 23e6186・push済み(origin/mainと同期確認済み)。詳細はLEARNINGS.md 2026-06-13参照
- 2026-06-12: B1「2D家具アイコンの質感改善」実装完了(優先度B/Cバックログより着手、sofa/bookcase/table・任意でlighting) — オーナー承認に基づき、優先度B/Cバックログ整理(2026-06-12)で挙げたB1に着手。優先6カテゴリ(bed/desk/chair/rug/tv_stand/storage_shelf)の専用Konvaアイコン化(2026-06-10)時点で未対応だったsofa/bookcase/table/lightingの4カテゴリに新規アイコンコンポーネントを実装し`FURNITURE_ICONS`に登録。①`SofaIcon.tsx`: 背もたれ・左右肘掛け・座面クッション3分割(折りジワ付き)で「濃い長方形+3矩形」から脱却 ②`BookcaseIcon.tsx`: 棚板フレーム・縦仕切り3区画・高さ違いの本の背表紙(ベージュ/グレージュ系)・足元影 ③`TableIcon.tsx`: 木目天板・縁のベベル・四隅の控えめな脚ヒントで「ボタン付きの板」感を解消 ④`LightingIcon.tsx`(任意): 既存の円形グローにリング+中心光源を追加(種類別分岐なし)。3D・保存データ構造・共有URLスキーマ・E2E仕様には変更なし。type-check pass・E2E 31/31 pass・preflight(34 PASS/0 FAIL/2 INFO)全PASS。10カテゴリ全体配置・Before/After(sofa/bookcase/table/lighting)・共有ページ・90度回転表示を含む8種のスクリーンショットを`screenshots/b1_icon_after/`に保存(`scripts/self-check-b1-icon-after.ts`、撮影後に一時スクリプトは削除)。オーナーレビュー結果: sofa(「濃い長方形」感が解消されソファと判別可能)/bookcase(本の背表紙で一目で本棚と分かる・改善幅大)/table(まだ地味だが「ボタン付きの板」感は弱まり許容ライン)/lighting(軽微な改善で問題なし)で合格(B1クローズ)。commit: a9fabb2・push済み(origin/mainと同期確認済み)。残課題(将来の任意改善・公開ブロッカーではない): ソファの色がやや冷たいグレー寄り、テーブルがまだ若干平面的、チェアのロボット感 — 優先度B/Cバックログに記録し今回スコープでは対応せず。詳細はLEARNINGS.md 2026-06-12参照
- 2026-06-12: Keepa API検証の事前準備完了(課金・実API実行・APIキー設定は今回も未実施) — オーナー指示「Keepa本検証にはまだ進まないが、課金後すぐ実行できる状態にする」に対応。①検証対象リストを`scripts/fixtures/keepa-targets.json`として新規作成(Amazon.co.jp家具40件=10カテゴリ×4件、旧20 ASINを維持+20件追加。ASINは実在確認未実施の想定例であることを`disclaimer`に明記) ②`scripts/verify-keepa.ts`をv3に改修し、`KEEPA_API_KEY`有無による`not_run`/`demo`/`real`の3モード制を導入(未設定時は実APIを呼ばず「未実施(NOT_RUN)」を全項目falseで出力しexit 0、`--demo`/`KEEPA_DEMO=1`は旧mockプレビューを`[DEMO]`表記・`source: mock_demo`として維持) ③結果フォーマットを13項目(ASIN/URL/カテゴリ/商品名・画像・価格・本体寸法・梱包寸法取得可否/取得寸法値/寸法種別/手動修正要否/エラー/判定メモ)に拡張し、JSON+新規CSV+新規Markdownレポートの3形式で`scripts/`に出力(全て`.gitignore`登録済み) ④採用判定基準(本体寸法取得率≥70%/50-69%/30-49%/<30%)はそのまま維持しつつ、`not_run`時は判定をスキップする分岐を追加 ⑤新規`docs/keepa-verification-targets.md`を作成し対象リスト・結果フォーマット・判定基準・実行手順(`verify-keepa`/`verify-keepa:demo`)を一元化、`docs/release-checklist.md`セクション7・`README.md`から参照リンクを追加。`scripts/package.json`に`verify-keepa:demo`スクリプト追加。type-check pass(verify-keepa.tsはエラー0件)・E2E/preflightは別途確認。**次のアクション**: オーナーがKeepa課金判断後、`scripts/fixtures/keepa-targets.json`のASIN実在確認→`KEEPA_API_KEY`設定→`pnpm --filter @fls/scripts verify-keepa`を実行するだけで本検証が完了する状態
- 2026-06-12: B2「人物の初期配置・重なり順改善」実装完了(優先度B/Cバックログより着手) — オーナー承認に基づき、調査結果どおり低リスク範囲で5点を実装。①`findFreeStandingPositionCm`を中心点判定からフットプリントAABB×家具/人物AABBの矩形重なり判定に変更(`getRotatedAABB`/`aabbOverlap`/`overlapsAnyRect`新設、既存家具+配置済み人物の両方を判定対象に追加) ②`addPerson`をstandingフットプリント(45×25cm)+10cmギャップ基準の部屋内グリッド探索に変更し、4人配置時の重なりを解消 ③`updatePersonPose`に新設`clampFootprintToRoomCm`を適用し、姿勢変更後のフットプリントが部屋外に突き出ないようクランプ(家具・他人物との重なり回避は対象外、今回はスコープ外として明示) ④`RoomCanvas2D`で選択中人物のみ描画順を最前面に回す`renderedPeople`を導入(people配列・保存・共有データの順序は不変) ⑤`PersonIcon2D`に`variant='shared'`を追加し共有ページの人物本体opacityを0.85〜0.95に向上、身長ラベルは小さく半透明(opacity 0.55)・常時表示で控えめに(家具の寸法ラベルは復活させていない)。type-check pass・E2E 31/31 pass・preflight(34 PASS/0 FAIL/2 INFO)全PASS。Before/After確認用スクリーンショット7枚を`screenshots/people_b2_after/`に保存(`scripts/self-check-people-b2-after.ts`)。commit: c71ba81・push済み(origin/mainと同期確認済み)。残課題: pose変更時の家具・他人物との自動重なり回避、chair/sofa/desk等へのスナップは未対応(スコープ外として明示)。詳細はLEARNINGS.md 2026-06-12参照
- 2026-06-12: UI改善フェーズクローズ＋優先度B/Cバックログ整理(ドキュメントのみ) — UI/UXポリッシュ第2弾(優先度A全8項目、commit c6243e7)のpush完了後、オーナー指示「Keepa API検証(課金判断要)には進まず、残課題を優先度B/Cでバックログ整理する」に対応。本ファイルに「UI/デザイン改善バックログ（優先度B/C・公開後改善候補）」セクションを新設し、8項目(B1:2D家具アイコン質感/B2:人物初期配置・重なり順/B3:LP独自性/C1:3D家具表現/C2:共有ページ見せ方/C3:モバイルフォールバック/C4:インテリアリスト価格表示/C5:3D壁床ラグ質感)を、目的・現状の問題・実装方針・今すぐやらない理由・着手タイミングの5項目で整理。`docs/release-checklist.md`にセクション14「公開判断マトリクスとUI/デザイン改善バックログ」を新設し、残作業全体を「公開ブロッカー」「公開前にできれば(任意)」「公開後改善でよい」「オーナー判断が必要」「自動で進められる」の5分類で整理(見た目の改善B1-C5と公開ブロッカーは別軸であることを明文化)。コード変更なし。詳細はLEARNINGS.md 2026-06-12「[決定]」エントリ参照
- 2026-06-12: 公開前preflightコマンド(pnpm run preflight) 実装完了 — オーナー指示「公開判断時に一発で実行できるpreflightコマンドを整備する」に対応。`scripts/preflight.ts`を新規作成し、root `package.json`に`preflight`スクリプト(`pnpm -C scripts run preflight`)、`scripts/package.json`に`preflight`スクリプト(`tsx preflight.ts`)を追加。①type-check(`pnpm run type-check`)②production build(`pnpm --filter web run build`)③E2E全件(`pnpm --filter web run test:e2e`)④release readiness self-check(`pnpm run self-check:release`)を順に実行し、いずれかが失敗(exit code≠0)した場合は以降を`[SKIP]`とし、最後に各ステップのPASS/FAIL/SKIPサマリと`Release preflight completed.\nReadiness report:\nfurniture-layout-simulator/screenshots/release_readiness/README.md`を表示する設計。初回実行は4ステップ全PASS: type-check PASS(@fls/shared・@fls/api・@fls/web 3パッケージ)、production build PASS(8ルート生成)、E2E 31/31 PASS(48.6s)、release readiness self-check 34 PASS/0 FAIL/2 INFO(INFO2件は`/terms`・`/privacy`の`【運営者名】`等プレースホルダー検出のみ・想定どおりオーナー判断待ち)。docs/release-checklist.mdにセクション13として実行コマンド・検証内容・失敗時に見る場所・レポート保存先・preflightでは判断できない項目(運営者名・問い合わせ先・管轄裁判所・正式ドメイン・GA4本番有効化・広告/アフィリエイト導入・Keepa API課金検証・法務文言最終妥当性)を追記。**今後、公開判断時は`pnpm run preflight`を実行しレポートを確認する**運用にする。Keepa API課金検証・GA4本番有効化・プレースホルダー確定・法務文言確定は今回も未対応(オーナー判断待ち)。commit: dbaa556・push済み
- 2026-06-12: リリース前自動検証スクリプト(self-check-release-readiness.ts) 実装完了 — オーナー指示「公開前プレースホルダー確定はやらず、毎回自動実行できるリリース前チェックを整備する」に対応。`scripts/self-check-release-readiness.ts`(Playwright直接操作)を新規作成し、`scripts/package.json`に`self-check:release`スクリプトを追加。本番相当設定(`NEXT_PUBLIC_ENABLE_URL_IMPORT=false`)のNext.js devサーバーを専用ポート(localhost:3100)で起動(既存サーバーがあれば再利用)し、①LP(`/`): 読み込み・desktop/mobile console errorなし・OGP系meta・robots(index可能)・GA4スクリプト未読込・/terms /privacyリンク・mobile 390px横スクロールなし、②Simulator(`/simulator`): 通常UI表示・Konva Canvas非0サイズ・/terms /privacyリンク・「+URL」が`url-import-disabled-message`で無効化・手動入力継続利用可・サンプル部屋読込・2D/簡易3D切替・共有URL生成・tablet(1023px)/mobile(390px)フォールバック表示、③Share(`/share`): 正常URL表示・リミックス導線・noindex維持・mobile崩れなし・不正hashでのエラー表示、④Terms/Privacy: 200表示・robots(index可能)・`【...】`プレースホルダー検出(検出のみ・置換せず)、を自動チェック。完了後`screenshots/release_readiness/README.md`にPASS/FAIL/INFO形式レポート+console error一覧+検出プレースホルダー一覧+スクリーンショット12枚を出力。初回実行は34/34 PASS(INFO2件は`/terms`・`/privacy`の`【運営者名】`等プレースホルダー検出=想定どおり)。プレースホルダーの中身確定・法務文言変更・GA4本番有効化・Keepa課金検証はこのスクリプトでは一切行わず、レポート末尾の「既知の残課題」に列挙するのみ。`pnpm --filter web run type-check`・E2E 31/31 pass。docs/release-checklist.mdに新セクション12として追記。**今後、公開直前には毎回`cd scripts && pnpm run self-check:release`を実行しレポートを確認すること**
- 2026-06-11: GA4/Analytics導入準備 完了(無効状態で実装) — UI/UXポリッシュ完了後、オーナー選択により次フェーズとして着手。`docs/release-checklist.md`セクション5の8イベント設計案を実装。新規`apps/web/src/lib/analytics/gtag.ts`(`GA_MEASUREMENT_ID = process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID`、`event(name, params)`ラッパー。ID未設定または`window.gtag`未定義時はno-op)・新規`apps/web/src/components/analytics/GoogleAnalytics.tsx`(ID未設定時は`null`を返しGA4スクリプト自体を読み込まない。設定時のみ`next/script`の`afterInteractive`でgtag.js+初期化スニペットを読込)を作成し、`layout.tsx`の`<head>`に追加。8イベントを各箇所に実装: `sample_room_loaded`(`handleLoadSample`)・`product_added_manual`(`ManualProductForm.tsx` `onSubmit`)・`furniture_placed`(`handleAddToCanvas`、`source`は`product.source==='amazon.co.jp' ? 'url' : 'manual'`で判定)・`layout_saved`(`handleSave`)・`share_url_created`(`handleShare`、`shareResult.ok`時のみ)・`share_page_opened`(`ShareView.tsx` payload復元成功時)・`remix_clicked`(`handleRemix`)・`view_3d_toggled`(`View3DToggle`の`onChange`呼び出し元)。`.env.example`に`NEXT_PUBLIC_GA_MEASUREMENT_ID=`を追加(本番有効化時の注意コメント付き)。**重要な依存関係**: `apps/web/src/app/privacy/page.tsx`は現状「アクセス解析ツール等は導入していません」と明記しているため、本番で`NEXT_PUBLIC_GA_MEASUREMENT_ID`を設定してGA4を有効化する際は、事前に`/privacy`セクション2・4の更新(取得情報の種類・利用目的の追記)と最終更新日の更新が必須。この「Analytics導入有無」の最終判断は、公開前プレースホルダー確定作業(正式サービス名・運営者名・問い合わせ先・管轄裁判所・正式ドメイン等)と合わせてオーナーが決定する。type-check pass・E2E 31/31 pass(現在は未設定のためGAスクリプト自体は読み込まれず、既存テストへの影響なし)。詳細は`docs/release-checklist.md`セクション5参照
- 2026-06-11: UI/UXポリッシュ(公開前最終調整) 完了 — オーナーレビューで承認された10項目(優先度A=必須4件、優先度B=任意6件)を実装。①LPモバイル(390px)で発生していた横スクロール(scrollWidth約1664px)を、ヒーローgridに`grid-cols-1 lg:grid-cols-12`+`min-w-0`を追加して解消(CSS Gridの子要素既定`min-width: auto`が原因)。②3D人物standingの胴体半径を`*0.8`→`*1.15`にして「青い柱」感を軽減。③2Dキャンバスの回転家具の寸法ラベルに、外接矩形(AABB)サイズを使った逆回転Group(`rotation={-rotationDeg}`)を適用し、回転角に関わらず常に正立・下端中央表示になるよう修正(0°時は元の表示と数式上完全一致することを確認)。④モバイルフォールバック見出しの不自然な改行(「編集」の途中で折り返し)を意味区切りの`<br />`で修正。⑤右パネル空状態に操作ヒント3項目を追加。⑥「人のスケール」カードの「+人を置く」ボタンを塗りつぶしからアウトラインに変更し主張を抑制。⑦3D壁面のambient/directionalライト色を暖色(`#FFF6EC`/`#FFEEDD`)に変更(wallColorデータ自体は変更せず)。⑧共有ページにブランドバッジ+新見出し「家具レイアウトの共有」+部屋サイズ入り説明文を追加。⑨共有ページのリミックスCTAを「このレイアウトを編集してみる」+「今の編集内容は置き換わります」に変更。⑩商品カードの「部屋に置く」ボタン(非選択時)を薄いテラコッタ背景+枠線付きに変更し視認性向上。type-check全パッケージpass・E2E 31/31 pass・LP mobile scrollWidth=390(オーバーフロー解消)を確認。Before/Afterスクリーンショットを`screenshots/ui_review_pass1/`(Before)・`screenshots/ui_review_pass2_after/`(After)に保存し全12画面を目視確認。撮影スクリプト`scripts/self-check-ui-review.ts`をコミット。優先度C項目・GA4・Keepa検証・Drawer化・3D大規模改善・新機能追加は今回スコープ外として明示的に対応せず。詳細は`docs/release-checklist.md`セクション11参照
- 2026-06-11: 利用規約・プライバシーポリシー・免責文言ページ ドラフト実装完了 — リリース前チェックリストの優先タスク（プライバシーポリシー→利用規約→免責文言→フッター導線→注意文言整理）に対応。共通レイアウト`apps/web/src/components/legal/LegalPageLayout.tsx`を新設し、`/terms`(利用規約、第1〜10条。免責事項は第6条に集約)・`/privacy`(プライバシーポリシー、サーバー保存なし・共有URL閲覧可能性・Analytics未導入を明記)を新規ページとして実装。LP(`/`)フッターに「利用規約」「プライバシーポリシー」リンク+免責一文、`/simulator`の部屋情報バーに小さなリンク、`/share`に新規フッター(「URLを知っている人なら誰でも閲覧できる」旨の注意+免責一文+リンク)を追加。サービス正式名称・運営者名・お問い合わせ先・準拠法管轄・ドメインが未確定のため、`【運営者名】`等のTODOプレースホルダーで実装し**最終公開前にオーナー確認必須**として明記。docs/release-checklist.mdに新セクション10として実装内容・残TODOを記録。type-check pass。GA4導入・Keepa API検証・Drawer化・3D改善・新機能追加は今回スコープ外として明示的に対応せず
- 2026-06-11: favicon・app icon・OGP/Twitter Card・metadataBase・noindex/index整理 完了 — リリース前チェックリストの優先度1範囲(favicon/app icon/basic metadata/OGP・Twitter Card土台/metadataBase/noindex・index現状整理)に対応。サービス名は仮名「家具レイアウトシミュレーター」のまま。`apps/web/src/lib/og/icon-mark.tsx`(共通アイコンマーク)・`icon.tsx`(favicon32×32)・`apple-icon.tsx`(180×180)・`lib/og/share-image.tsx`(OGP/Twitter共通1200×630のフロアプラン風グラフィック)・`opengraph-image.tsx`/`twitter-image.tsx`を`next/og`の`ImageResponse`で新規作成。Satori(next/ogのレンダラ)は日本語フォントを標準搭載しないため、全画像をテキストなし・Warm Editorialパレットの図形のみで構成(タイトル・説明文はSNS側が`og:title`/`og:description`の通常metaタグから表示するため日本語でも問題なし)。root `layout.tsx`に`metadataBase`(`NEXT_PUBLIC_SITE_URL`環境変数、未設定時`http://localhost:3000`にフォールバック)・`applicationName`・`openGraph`・`twitter`・`viewport`(themeColor)を追加。**重大な発見**: root `layout.tsx`に`robots: { index: false, follow: false }`がグローバル設定されており、LP `/`を含む全ページがnoindexになっていたバグを発見・修正(グローバル`robots`を削除しデフォルトのindex/followに)。`/share`・`/simulator`は各ページの個別`robots`設定でnoindex維持(`/simulator`は将来index化を検討する旨をdocs/release-checklist.mdに記録)。`.env.example`に`NEXT_PUBLIC_SITE_URL`追加。type-check・`next build`・本番サーバーでの実機確認(favicon/apple-icon/OGP画像の目視・`/`/`/simulator`/`/share`のmeta robots/og:タグ確認)済み
- 2026-06-11: `/simulator` 1024px未満フォールバック拡大 完了 — 前回のオーナーレビューで「768×900の通常UI表示は窮屈」と指摘された残課題に対応。改善候補①(フォールバック対象を1024px未満に拡大)を採用し、②(左右パネルのDrawer化)は設計変更が大きいため見送り。`SimulatorLayout`の判定を`window.matchMedia('(max-width: 767px)')`から`window.matchMedia('(max-width: 1023px)')`に変更し、変数名も`isMobile`→`isCompactViewport`に改名(1024px未満には縦向きタブレットも含まれ「モバイル」という呼称が実態と合わなくなったため)。`SimulatorMobileFallback`の文言を「PC・タブレットでの編集に対応」→「PC・横向きタブレットでの編集に対応」に調整し、スマートフォン/縦向きタブレットでは編集非対応・共有ページ閲覧は可能という方針を明確化。`mobile-fallback.spec.ts`を4件→7件に全面改訂し、390/575/768/1023pxのフォールバック表示と1024/1440pxの通常表示、計6境界点を個別テスト化。`scripts/self-check-mobile-fix.ts`・`screenshots/review_after_mobile_fix/`も新境界に合わせて更新(768×900・1023×900のフォールバック画面、1024×900の通常画面を再撮影)。type-check pass・E2E 31/31 pass。Keepa API検証・Drawer化・3D改善・LP刷新・新機能追加は今回スコープ外として明示的に対応せず
- 2026-06-11: `/simulator` モバイル幅クラッシュ修正・本番公開前安全化 完了 — 前回のvisual reviewで発見された最重要バグ(画面幅576px以下で`/simulator`が完全クラッシュ)を修正。原因は左サイドバー(320px)+右パネル(256px)=576pxの固定幅により、576px以下では中央`canvas-area`の幅が0以下になり、react-konvaの`Stage`がwidth/height 0のcanvasに`drawImage`して`InvalidStateError`が発生し、Next.jsエラーオーバーレイで画面がほぼ無地になっていたこと。対策として①新規`SimulatorMobileFallback`コンポーネントを作成し、768px未満では3ペイン編集UI・2D/3D Canvasを一切マウントせずPC/タブレット推奨の案内画面(「シミュレーターはPC・タブレットでの編集に対応しています」+トップへ戻るボタン)を表示する方式に変更(`window.matchMedia`で判定、SSR/初回レンダリングはどちらの分岐にも倒れない中立な空画面を返しハイドレーション不一致を回避) ②新規`useElementSize`フック(ResizeObserver)を作成し、RoomCanvas2D・Room3DSceneの両方でcanvasコンテナの実寸が0以下の間はStage/Canvasを描画せず「画面サイズを広げてください」プレースホルダーを表示する防御を追加(`Math.max(width,1)`のような誤魔化しは不使用、768px以上でも理論上の防御として機能) ③ついでにMockProviderの本番安全化も実施: `NEXT_PUBLIC_ENABLE_URL_IMPORT`フラグ(本番デフォルトOFF)で「+URL」入力を「URLからの自動取得は準備中です。現在は手動入力をご利用ください。」表示に切替え、APIサーバー側(`apps/api/src/routes/parse.ts`)も本番+MockProvider時はURL取り込みをブロックして準備中メッセージを返すようにした(手動入力は影響なし)。E2Eを23→28件に拡張(モバイルフォールバック4件+URL取り込み無効化1件)、全件pass。type-check全パッケージpass。`screenshots/review_after_mobile_fix/`に7画面の検証スクリーンショット+READMEを作成。Keepa API検証・3D改善・LPデザイン改善・新機能追加は今回スコープ外として明示的に対応せず
- 2026-06-11: 「人のスケール」オーナーレビューフィードバック対応完了 — スクリーンショットレビューで指摘された4点(必須2件・任意2件)に対応。①standing(立つ)を新規配置時に家具と重ならない床上の位置へ自動配置する機能(`findFreeStandingPositionCm`)を追加し、「ベッドの上に立っている」ように見える視覚的不自然さを解消(高さ計算ロジック自体は元々正しく床基準だった) ②共有URL長すぎエラーの文言を「家具数が多すぎるため共有URLを作成できません」から「共有URLが長すぎます。家具・人・商品名を減らしてください。」に変更し原因を限定しすぎないようにした ③2D人物アイコンを非選択時は透明度・ラベルサイズを抑えて家具の視認性を確保(lyingは特に控えめ) ④3D人物モデルのstanding胴体を細く・頭身比率を自然に・配色を落ち着いたグレイッシュブルー2色に・sittingに脚を追加して着座を分かりやすく。Playwrightセルフチェックスクリプト(scripts/self-check-people.ts)を新規追加してコミット。type-check pass・E2E 23/23 pass・self-check全項目OK確認。commit: 21827e5・push済み
- 2026-06-11: 「人のスケール」機能（複数人・姿勢対応） 実装完了 — オーナー承認の最終仕様（「自分を置く」案から「人のスケール」実用機能に変更）に基づき実装。最大4人(MAX_PEOPLE=4)を部屋に配置可能、各人物は身長(120-220cm,初期170cm)・姿勢(立つ/座る/寝る)・位置・90度回転を個別設定できる。`PersonInstance`型は`furniture[]`・買い物リストとは完全分離した独立配列`people?: PersonInstance[]`として`LayoutData`/`SharedLayoutPayload`にoptionalフィールド追加（既存データ・既存共有URLとの後方互換維持）。2D(react-konva)は姿勢別アイコン(standing/sitting/lyingで形状差別化、lyingのみ身長に応じて footprint長が変化)、3D(@react-three/fiber)はcylinderGeometry+sphereGeometryの組み合わせ(capsuleGeometry不使用)で姿勢別簡易モデルを表示。3Dでは「簡易的」なAABB判定により、寝た人物がbed/sofa上にいれば家具高さ分かさ上げ、座った人物がchair/sofa上にいれば座面高さで表示(該当家具がなければ床基準)。左パネルに「人のスケール」カード(折りたたみ式・最大4人で追加ボタン無効化)を家具リストと視覚的に分離して配置、PropertiesPanelに専用パネル(身長スライダー・姿勢切替・回転・削除)を追加。localStorage保存/復元・共有URL/リミックスでも人物情報を維持。E2Eを17→23件に拡張、型チェック・全件pass。Keepa API有償検証は引き続きリリース前必須タスクとして別管理
- 2026-06-11: 簡易3Dプレビュー機能 実装完了 — Keepa API有償検証は後回しとし、無料で進められる優先タスクとして着手。@react-three/fiber+drei+three.jsで2D配置データ(部屋寸法・家具位置/回転/寸法/カテゴリ)を箱型3Dモデルに変換して描画。床+壁2面(北・西)+家具直方体(高さ反映・カテゴリ別配色)+OrbitControls実装。ツールバーに2D/3D切替トグルを追加し、既存のKonva 2D編集体験はそのまま維持(状態はeditorStoreで共有)。RoomViewer(2D)と同じくstore非依存の汎用コンポーネント設計とし、将来`/share`ページへの3D対応も追加実装のみで可能。WebGL非対応環境向けにError Boundaryでフォールバック表示を用意。E2Eを15→17件に拡張、全通過。self-check-3d.tsでサンプル部屋(6家具)の2D→3D→OrbitControlsドラッグ回転→2D復帰までスクリーンショット取得し目視確認、表示・配色・回転とも正常動作を確認
- 2026-06-10: 匿名共有URL機能 手動実機確認完了 — Playwrightセルフチェックスクリプト(scripts/self-check-share.ts、リポジトリにコミット・push済み)で6シーン（①サンプル部屋読込②共有ポップオーバー③共有ページ④インテリアリスト⑤リミックスCTA⑥リミックス後/simulator）をスクリーンショット撮影し目視確認。E2E未カバーだったリミックスボタン押下→`/simulator`遷移→家具6件（寸法も一致）の復元まで含め全て正常動作を確認、問題なし。匿名共有URL機能はこれでE2E+手動確認の両面で完了
- 2026-06-10: 匿名共有URL機能 実装完了 — `/share#data=<encoded>`のhash fragment方式（バックエンド・DB不要、サーバーログにレイアウトデータが残らない）。packages/sharedにSharedLayoutPayload型+zodバリデーション(items最大50件・寸法/座標範囲チェック)追加、lz-stringで圧縮、URL長2000文字超は「家具数が多すぎるため共有URLを作成できません」と表示して発行しない。ペイロードに個人情報（レイアウト名・ユーザー名・住所・メモ）は含めない方針を徹底。共有ポップオーバーに「このURLを知っている人はレイアウトを閲覧できます」と明記。共有ページはRoomViewer（LPのRoomSceneと共通化）+SharedItemListで表示、noindex維持。decode失敗・不正hash・50件超・巨大payloadは全てクラッシュせずエラー画面を表示。「このレイアウトを自分の部屋として開く」リミックスは既存レイアウトを上書き（「現在の作業内容を置き換えて開きます」と明示）。E2E 13→15件に拡張、全通過
- 2026-06-10: 見た目の質感・プロダクト感の微調整完了 — オーナーレビューで「チェアの記号感」「ラグの主張過多」「ベージュ/テラコッタ寄りの配色」「LPヒーローのアプリ作例感」「CTAボタンの強弱」の5点を指摘され、大改修ではなく微調整で対応。チェア再設計(座面/背もたれ/肘掛け/キャスターを自然な配置に)、ラグ減色、パレットをウォルナット/チャコール寄りに、LPヒーロー拡大(6:6カラム+bleed)、商品カードCTAを状態依存デザインに変更。E2E 13/13 pass。共有URL実装前の「人に見せても恥ずかしくない見た目」ラインに到達
- 2026-06-10: Priority-A追加対応完了 — 「AI生成っぽいテンプレ感」解消のため、bed/desk/chair/rug等の家具マーカーをディテール刷新（特にchairは放射状ラインのX字見えを修正、rugは縁取り+中央メダリオンに変更）、選択枠を上品なテラコッタグローに、キャンバス(壁・グリッド・床・窓ドア表示)をsofterに、サンプルレイアウトを非重複の「住みたくなる」配置に再構成、ヒーローモックアップ全面差し替え。E2E 13/13 pass
- 2026-06-10: Priority-A UI改善完了 — 家具ビジュアル(cornerRadius・シャドウ・選択枠)、サンプル部屋6点化(収納棚・テレビ台・ラグ・デスク・チェア追加)、インテリアリスト見出し、ヒーローモックアップ刷新。E2E 13/13 pass
- 2026-06-09: 家具レイアウトシミュレーター GitHub push完了 (https://github.com/noregista/furniture-layout-simulator) — MVP Day1〜7・E2E 10/10・README整備


- 2026-04-14: 水無月澪（スピリチュアル占い）Threadsアカウント新設・spiritual_writer.py構築・初投稿完了
- 2026-04-14: writer.py バグ修正（spiritualアカウントへのニュース誤割り当て）
- 2026-04-14: Meta for Developers 新アプリ設定完了（C/D/E/H トークン再発行済み）
- 2026-04-12: check_health.sh 作成（Threads/KDP/Git の稼働状態一括チェック）
- 2026-04-12: monthly_kpi.py 作成（月次KPI自動集計 → KPI_YYYY_MM.md 出力）
- 2026-04-12: optimize_post_times.py 作成（analyst_feedback.jsonから最適投稿時間を自動更新）
- 2026-04-12: 投稿時間をlaunchd起動時刻に合わせて修正（09:00/12:00/21:00）
- 2026-04-12: Threads config.json をサブモジュールに統一（旧threads_botから移行）
- 2026-04-12: KDP初回出版申請（ChatGPT・Claude完全攻略ガイド ¥980）審査中
- 2026-04-12: fal.ai高品質表紙生成・transfer_to_windows.sh・record_asin.py 実装
- 2026-04-12: KDP_upload_guide.md（次回から画像不要で設定完了できるガイド）作成
- 2026-04-12: KDPアカウント開設・銀行口座・税務情報（W-8BEN）登録完了
- 2026-04-12: 04_KDP_Automation パイプライン初期構築
- 2026-04-11: writer.py バズサーチデータ全件適用
- 2026-04-11: LEARNINGS.md・Business-Tracker.md 導入
- 2026-04-10: trend_guide.json 初回生成（バズサーチ稼働確認）
- 2026-04-10: セキュリティ対応（config.json Git除外）
- 2026-04-10: 会社ディレクトリ・CLAUDE.md 初期構築

---

*初版作成: 2026-04-11 | AI統括マネージャー*
