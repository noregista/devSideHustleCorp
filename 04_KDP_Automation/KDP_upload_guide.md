# KDP アップロードガイド（完全版）

## epub転送手順（Mac → Windows）

Macで実行：
```bash
cd ~/dev/devSideHustleCorp/04_KDP_Automation
sed -i '' 's|^output/$|#output/|' .gitignore
git add output/*.epub output/*.jpg output/KDP_upload_info.md .gitignore
git commit -m "[KDP] epub一時転送"
git push
```

Windowsで実行（Claude Codeに頼む）：
```bash
git pull
```

---

## Step 1：Kindle本の詳細

| 項目 | 設定値 |
|------|--------|
| 言語 | 日本語 |
| タイトルフリガナ | カタカナで入力 |
| タイトルローマ字 | 英字で入力（記号不可） |
| サブタイトル・シリーズ・レーベル・版 | 全て空欄 |
| 主な著者氏名 | （book_history.jsonのauthorを参照） |
| 著者フリガナ | カタカナ |
| 著者ローマ字 | 例）Yamazaki Takumi |
| 内容紹介 | book_history.jsonのdescriptionを貼り付け |
| 権利 | 「私は著作権者であり〜」を選択 |
| 露骨な性的表現 | いいえ |
| 対象年齢 | 空欄 |
| 主なマーケットプレイス | Amazon.co.jp |

### カテゴリー設定
1. `ビジネス・経済` → `業務改善`
2. `コンピュータ・IT` → `一般・入門書` → `その他の入門書`

### キーワード（book_history.jsonのkeywordsを使用）
7つのボックスに1つずつ入力。

### 本の発売オプション
`本の発売準備ができました` を選択

---

## Step 2：Kindle本のコンテンツ

| 項目 | 設定値 |
|------|--------|
| ページを読む方向 | 左から右（横書き） |
| DRM | はい（適用する） |
| 原稿アップロード | output/ のepubファイル |
| 表紙アップロード | Canvaで作成した画像（1600×2560px推奨） |
| AI生成コンテンツ | はい |
| ISBN・出版社・主コード | 全て空欄 |
| アクセシビリティ | スキップ |

### 表紙作成（Canva）
1. canva.com → サイズ 1600×2560px で新規作成
2. 以下のプロンプトをCanva AIに入力：
   ```
   Kindle電子書籍の表紙。タイトル「{タイトル}」、著者名「{著者名}」。
   プロフェッショナルなビジネス書デザイン。青・黒を基調としたモダンなデザイン。
   日本語テキスト。縦長フォーマット。
   ```
3. JPGでダウンロード → KDPにアップロード

---

## Step 3：価格設定

| 項目 | 設定値 |
|------|--------|
| KDPセレクト | 登録しない |
| 出版地域 | すべての地域（全世界） |
| ロイヤリティ | 70% |
| Amazon.co.jp価格 | book_history.jsonのprice_jpyを入力 |

→ 他マーケットプレイスは自動計算される

---

## アカウント設定（初回のみ・設定済み）

- 事業の種類：個人
- 銀行口座：日本（JPY）登録済み
- Amazon.com.br：小切手払い設定済み
- 税務情報（W-8BEN）：署名済み

---

## 出版後の作業

1. 72時間後にAmazon.co.jpで販売確認
2. ASINをURLから取得（例：`B0XXXXXXXX`）
3. Claude Codeに「ASINは〇〇です」と伝える → book_history.json更新

---

## epub転送後のクリーンアップ（Windows側で実行）

KDPアップロード完了後：
```bash
cd c:/dev/devSideHustleCorp/04_KDP_Automation
git rm output/*.epub output/*.jpg output/KDP_upload_info.md
git commit -m "[KDP] epub・表紙・投稿情報をGit管理から除外"
git push
```
