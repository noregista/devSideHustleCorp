# 04_KDP_Automation — CLAUDE.md

## 概要
Amazon KDP（Kindle Direct Publishing）向け電子書籍を自動生成するパイプライン。
週1サイクルで「トレンドリサーチ → テーマ選定 → 本文生成 → epub出力」を全自動化する。
KDPへのアップロードのみオーナーが手動で行う（約15分）。

## パイプライン構成

```
researcher.py  → トレンドリサーチ（Claude Haiku）
scorer.py      → テーマスコアリング・選定（Claude Haiku）
writer.py      → 本文生成・章ごとに分割生成（Claude Sonnet）
formatter.py   → epub変換・表紙生成（ebooklib + Pillow）
main.py        → 全体オーケストレーション
```

## ジャンル方針
- ジャンルは固定しない。毎回リサーチで最も売れやすいテーマを選ぶ
- 日本語Amazon KDP市場をターゲット

## 出力
- `output/` に epub ファイルを保存
- `book_history.json` に生成・出版履歴を記録
- `research_cache/` にリサーチ結果をキャッシュ（再利用可能）

## 注意
- config.json は .gitignore 対象（APIキーを含むため）
- KDP出版後はbook_history.jsonにASIN・価格・出版日を記録すること
