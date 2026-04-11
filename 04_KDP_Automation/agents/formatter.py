"""
agents/formatter.py

本文テキストをepubファイルに変換する。
表紙画像もPillowで自動生成する。

依存: ebooklib, Pillow
インストール: pip install ebooklib Pillow
"""

from __future__ import annotations

import logging
import re
import textwrap
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
import uuid

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
JST = timezone(timedelta(hours=9))


def _markdown_to_html(text: str) -> str:
    """簡易Markdown → HTML変換（見出し・段落・箇条書き対応）"""
    lines = text.split("\n")
    html_lines = []
    in_ul = False

    for line in lines:
        # h1
        if line.startswith("# "):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            html_lines.append(f"<h1>{line[2:].strip()}</h1>")
        # h2
        elif line.startswith("## "):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            html_lines.append(f"<h2>{line[3:].strip()}</h2>")
        # h3
        elif line.startswith("### "):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            html_lines.append(f"<h3>{line[4:].strip()}</h3>")
        # 箇条書き
        elif re.match(r'^[-・]\s', line):
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            html_lines.append(f"<li>{line[2:].strip()}</li>")
        # 番号付きリスト
        elif re.match(r'^\d+\.\s', line):
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            content = re.sub(r'^\d+\.\s', '', line).strip()
            html_lines.append(f"<li>{content}</li>")
        # 空行
        elif line.strip() == "":
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            html_lines.append("")
        # 通常段落
        else:
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            html_lines.append(f"<p>{line.strip()}</p>")

    if in_ul:
        html_lines.append("</ul>")

    return "\n".join(html_lines)


def generate_cover_image(title: str, author: str, output_path: Path) -> bool:
    """Pillowで表紙画像を生成する（1600x2560px）"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        logging.warning("Pillowがインストールされていません。表紙生成をスキップします。")
        return False

    W, H = 1600, 2560
    img = Image.new("RGB", (W, H), color=(25, 25, 60))
    draw = ImageDraw.Draw(img)

    # 背景グラデーション風の装飾
    for i in range(0, H, 4):
        alpha = int(30 * (1 - i / H))
        draw.line([(0, i), (W, i)], fill=(255, 255, 255, alpha), width=1)

    # アクセントライン
    draw.rectangle([80, 80, W - 80, 90], fill=(255, 200, 50))
    draw.rectangle([80, H - 90, W - 80, H - 80], fill=(255, 200, 50))

    # タイトルテキスト（フォントがなければデフォルト使用）
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 80)
        font_author = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", 48)
    except Exception:
        try:
            font_title = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 80)
            font_author = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 48)
        except Exception:
            font_title = ImageFont.load_default()
            font_author = ImageFont.load_default()

    # タイトルを折り返してセンタリング
    title_lines = textwrap.wrap(title, width=12)
    y = H // 3
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y), line, font=font_title, fill=(255, 255, 255))
        y += 100

    # 著者名
    bbox = draw.textbbox((0, 0), author, font=font_author)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 200), author, font=font_author, fill=(200, 200, 200))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), "JPEG", quality=95)
    logging.info(f"表紙画像生成: {output_path}")
    return True


def build_epub(book_data: dict, kdp_metadata: dict, output_dir: Path = OUTPUT_DIR) -> Optional[Path]:
    """
    book_dataからepubを生成する。

    book_data: writer.pyが返す dict
      {
        "outline": {...},
        "chapters": [{"label": "はじめに", "title": "...", "content": "..."}],
        "total_chars": 12345
      }
    kdp_metadata: scorer.pyが返す dict
      {
        "price_jpy": 500,
        "categories": [...],
        "keywords": [...],
        "description": "..."
      }
    """
    try:
        from ebooklib import epub
    except ImportError:
        logging.error("ebooklibがインストールされていません。pip install ebooklib を実行してください。")
        return None

    outline = book_data.get("outline", {})
    chapters = book_data.get("chapters", [])
    title = outline.get("title", "無題")
    author = outline.get("author", "著者名")

    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(title)
    book.set_language("ja")
    book.add_author(author)

    # 表紙画像
    output_dir.mkdir(parents=True, exist_ok=True)
    cover_path = output_dir / f"cover_{datetime.now(tz=JST).strftime('%Y%m%d_%H%M%S')}.jpg"
    if generate_cover_image(title, author, cover_path):
        with open(cover_path, "rb") as f:
            cover_data = f.read()
        book.set_cover("cover.jpg", cover_data)

    # CSSスタイル
    css_content = """
body { font-family: 'ヒラギノ角ゴシック', 'Meiryo', sans-serif; line-height: 1.8; margin: 5%; }
h1 { font-size: 1.6em; border-bottom: 2px solid #333; padding-bottom: 0.3em; margin-top: 2em; }
h2 { font-size: 1.3em; margin-top: 1.5em; color: #1a1a60; }
h3 { font-size: 1.1em; margin-top: 1.2em; }
p { text-indent: 1em; margin: 0.5em 0; }
ul { margin: 0.5em 0 0.5em 2em; }
li { margin: 0.3em 0; }
"""
    css = epub.EpubItem(uid="style", file_name="style.css", media_type="text/css", content=css_content)
    book.add_item(css)

    # 各章をepubアイテムに変換
    epub_chapters = []
    for i, ch in enumerate(chapters):
        html_content = _markdown_to_html(ch["content"])
        item = epub.EpubHtml(
            title=ch["title"],
            file_name=f"chapter_{i:02d}.xhtml",
            lang="ja",
        )
        item.content = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja">
<head>
  <meta charset="utf-8"/>
  <title>{ch['title']}</title>
  <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
{html_content}
</body>
</html>"""
        item.add_item(css)
        book.add_item(item)
        epub_chapters.append(item)

    # 目次・スパイン
    book.toc = [(epub.Section(ch["title"]), [item]) for ch, item in zip(chapters, epub_chapters)]
    book.spine = ["nav"] + epub_chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # 出力
    timestamp = datetime.now(tz=JST).strftime("%Y%m%d_%H%M%S")
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)[:40]
    output_path = output_dir / f"{timestamp}_{safe_title}.epub"
    epub.write_epub(str(output_path), book)
    logging.info(f"epub生成完了: {output_path}")
    return output_path


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("formatter.py: epubライブラリの動作確認")
    try:
        from ebooklib import epub
        print("✅ ebooklib OK")
    except ImportError:
        print("❌ ebooklib未インストール → pip install ebooklib")
    try:
        from PIL import Image
        print("✅ Pillow OK")
    except ImportError:
        print("❌ Pillow未インストール → pip install Pillow")
