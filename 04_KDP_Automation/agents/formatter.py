"""
agents/formatter.py

本文テキストをepubファイルに変換する。
表紙: fal.ai（flux-pro）でAI背景生成 → Pillowで日本語テキスト合成
フォールバック: Pillowのみで生成

依存: ebooklib, Pillow, fal-client, requests
インストール: pip install ebooklib Pillow fal-client requests
"""

from __future__ import annotations

import logging
import os
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
        if line.startswith("# "):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            html_lines.append(f"<h1>{line[2:].strip()}</h1>")
        elif line.startswith("## "):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            html_lines.append(f"<h2>{line[3:].strip()}</h2>")
        elif line.startswith("### "):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            html_lines.append(f"<h3>{line[4:].strip()}</h3>")
        elif re.match(r'^[-・]\s', line):
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            html_lines.append(f"<li>{line[2:].strip()}</li>")
        elif re.match(r'^\d+\.\s', line):
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            content = re.sub(r'^\d+\.\s', '', line).strip()
            html_lines.append(f"<li>{content}</li>")
        elif line.strip() == "":
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            html_lines.append("")
        else:
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            html_lines.append(f"<p>{line.strip()}</p>")

    if in_ul:
        html_lines.append("</ul>")

    return "\n".join(html_lines)


def _get_font(size: int):
    """日本語フォントを取得する（Mac / Windows 対応）"""
    from PIL import ImageFont
    font_candidates = [
        # Mac
        "/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/Library/Fonts/NotoSansCJKjp-Bold.otf",
        # Windows
        "C:/Windows/Fonts/meiryob.ttc",
        "C:/Windows/Fonts/meiryo.ttc",
        "C:/Windows/Fonts/YuGothB.ttc",
        "C:/Windows/Fonts/YuGothic.ttf",
    ]
    for path in font_candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _generate_cover_background_fal(title: str, genre: str, fal_key: str, output_path: Path) -> bool:
    """fal.ai（flux-pro）でプロ品質の表紙背景画像を生成する"""
    try:
        import fal_client
        import requests
    except ImportError:
        logging.warning("fal-client または requests が未インストールです。pip install fal-client requests")
        return False

    os.environ["FAL_KEY"] = fal_key

    # ジャンルに応じたスタイル指示
    style_map = {
        "ビジネス": "modern corporate dark navy blue background, gold accent lines, abstract geometric shapes, professional atmosphere",
        "AI": "dark tech background, glowing blue neural network patterns, digital circuits, futuristic atmosphere",
        "投資": "dark finance background, subtle gold coins, stock chart lines, wealth and prosperity atmosphere",
        "健康": "clean white and green gradient, minimalist zen design, fresh and calming atmosphere",
        "自己啓発": "inspiring gradient from dark blue to purple, light rays, motivational atmosphere",
    }
    genre_key = next((k for k in style_map if k in genre), None)
    bg_style = style_map.get(genre_key, "professional dark gradient background, elegant minimalist design, premium book cover atmosphere")

    prompt = (
        f"Professional Kindle ebook cover background for Japanese market. "
        f"{bg_style}. "
        f"NO text, NO letters, NO words. Pure background only. "
        f"High quality, 4K, dramatic lighting, publisher quality."
    )

    logging.info(f"fal.ai で表紙背景を生成中...")
    try:
        result = fal_client.run(
            "fal-ai/flux-pro",
            arguments={
                "prompt": prompt,
                "image_size": {"width": 1600, "height": 2560},
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
                "num_images": 1,
                "safety_tolerance": "2",
            }
        )
        image_url = result["images"][0]["url"]
        resp = requests.get(image_url, timeout=60)
        resp.raise_for_status()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(resp.content)
        logging.info(f"fal.ai 背景生成完了: {output_path}")
        return True
    except Exception as e:
        logging.warning(f"fal.ai 生成失敗: {e}")
        return False


def _overlay_text_on_cover(bg_path: Path, title: str, author: str, output_path: Path) -> bool:
    """背景画像の上に日本語テキスト（タイトル・著者名）を合成する"""
    try:
        from PIL import Image, ImageDraw, ImageFilter
    except ImportError:
        return False

    W, H = 1600, 2560
    img = Image.open(bg_path).convert("RGB").resize((W, H))
    draw = ImageDraw.Draw(img)

    # 下部に半透明の暗いオーバーレイ（テキスト可読性向上）
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.rectangle([0, H // 2, W, H], fill=(0, 0, 0, 160))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # アクセントライン
    draw.rectangle([60, 60, W - 60, 68], fill=(255, 200, 50))
    draw.rectangle([60, H - 68, W - 60, H - 60], fill=(255, 200, 50))

    # タイトル（折り返し・センタリング）
    font_title = _get_font(88)
    font_author = _get_font(52)

    # タイトルを1行12文字で折り返し
    title_lines = []
    chunk = ""
    for ch in title:
        chunk += ch
        if len(chunk) >= 12 or ch in "。、！？":
            title_lines.append(chunk)
            chunk = ""
    if chunk:
        title_lines.append(chunk)

    # タイトルを中央より少し上に配置
    total_h = len(title_lines) * 110
    y = (H - total_h) // 2 - 80
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        tw = bbox[2] - bbox[0]
        # テキストシャドウ
        draw.text(((W - tw) // 2 + 3, y + 3), line, font=font_title, fill=(0, 0, 0, 180))
        draw.text(((W - tw) // 2, y), line, font=font_title, fill=(255, 255, 255))
        y += 110

    # 著者名（下部）
    author_text = f"著: {author}"
    bbox = draw.textbbox((0, 0), author_text, font=font_author)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2 + 2, H - 170 + 2), author_text, font=font_author, fill=(0, 0, 0, 180))
    draw.text(((W - tw) // 2, H - 170), author_text, font=font_author, fill=(220, 220, 220))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), "JPEG", quality=95)
    logging.info(f"テキスト合成完了: {output_path}")
    return True


def generate_cover_image(title: str, author: str, genre: str, output_path: Path, fal_key: str = "") -> bool:
    """
    表紙画像を生成する。
    fal_key があれば fal.ai で高品質背景生成 → Pillow でテキスト合成。
    なければ Pillow のみで生成。
    """
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        logging.warning("Pillowが未インストールです。pip install Pillow")
        return False

    bg_path = output_path.with_suffix(".bg.jpg")
    fal_success = False

    if fal_key:
        fal_success = _generate_cover_background_fal(title, genre, fal_key, bg_path)

    if fal_success:
        # fal.ai背景 + Pillowテキスト合成
        result = _overlay_text_on_cover(bg_path, title, author, output_path)
        # 一時背景ファイルを削除
        if bg_path.exists():
            bg_path.unlink()
        if result:
            return True
        logging.warning("テキスト合成失敗。Pillowフォールバックへ")

    # フォールバック: Pillowのみ
    return _generate_cover_pillow_only(title, author, output_path)


def _generate_cover_pillow_only(title: str, author: str, output_path: Path) -> bool:
    """Pillowのみで表紙を生成するフォールバック"""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return False

    W, H = 1600, 2560
    img = Image.new("RGB", (W, H), color=(18, 28, 72))
    draw = ImageDraw.Draw(img)

    # グラデーション風背景
    for i in range(H):
        ratio = i / H
        r = int(18 + (45 - 18) * ratio)
        g = int(28 + (20 - 28) * ratio)
        b = int(72 + (100 - 72) * ratio)
        draw.line([(0, i), (W, i)], fill=(r, g, b))

    draw.rectangle([60, 60, W - 60, 68], fill=(255, 200, 50))
    draw.rectangle([60, H - 68, W - 60, H - 60], fill=(255, 200, 50))

    font_title = _get_font(88)
    font_author = _get_font(52)

    title_lines = textwrap.wrap(title, width=12) or [title]
    y = H // 3
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y), line, font=font_title, fill=(255, 255, 255))
        y += 110

    author_text = f"著: {author}"
    bbox = draw.textbbox((0, 0), author_text, font=font_author)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 170), author_text, font=font_author, fill=(200, 200, 200))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), "JPEG", quality=95)
    logging.info(f"表紙生成（Pillowフォールバック）: {output_path}")
    return True


def build_epub(book_data: dict, kdp_metadata: dict, output_dir: Path = OUTPUT_DIR, fal_key: str = "") -> Optional[Path]:
    """
    book_dataからepubを生成する。

    book_data: writer.pyが返す dict
    kdp_metadata: scorer.pyが返す dict
    fal_key: fal.ai APIキー（空の場合はPillowフォールバック）
    """
    try:
        from ebooklib import epub
    except ImportError:
        logging.error("ebooklibが未インストールです。pip install ebooklib を実行してください。")
        return None

    outline = book_data.get("outline", {})
    chapters = book_data.get("chapters", [])
    title = outline.get("title", "無題")
    author = outline.get("author", "著者名")
    genre = outline.get("genre", "ビジネス")

    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(title)
    book.set_language("ja")
    book.add_author(author)

    # 表紙画像（fal.ai + Pillow合成 or Pillowフォールバック）
    output_dir.mkdir(parents=True, exist_ok=True)
    cover_path = output_dir / f"cover_{datetime.now(tz=JST).strftime('%Y%m%d_%H%M%S')}.jpg"
    if generate_cover_image(title, author, genre, cover_path, fal_key=fal_key):
        with open(cover_path, "rb") as f:
            cover_data = f.read()
        book.set_cover("cover.jpg", cover_data)

    # CSSスタイル
    css_content = """
body { font-family: 'ヒラギノ角ゴシック', 'Meiryo', 'YuGothic', sans-serif; line-height: 1.8; margin: 5%; }
h1 { font-size: 1.6em; border-bottom: 2px solid #333; padding-bottom: 0.3em; margin-top: 2em; }
h2 { font-size: 1.3em; margin-top: 1.5em; color: #1a1a60; }
h3 { font-size: 1.1em; margin-top: 1.2em; }
p { text-indent: 1em; margin: 0.5em 0; }
ul { margin: 0.5em 0 0.5em 2em; }
li { margin: 0.3em 0; }
"""
    css = epub.EpubItem(uid="style", file_name="style.css", media_type="text/css", content=css_content)
    book.add_item(css)

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
</html>""".encode("utf-8")
        item.add_item(css)
        book.add_item(item)
        epub_chapters.append(item)

    # 巻末シリーズリンクページ
    series_section = book_data.get("series_section", "")
    if series_section and series_section.strip():
        series_html = _markdown_to_html(series_section.strip())
        series_item = epub.EpubHtml(
            title="このシリーズの他の作品",
            file_name="series_links.xhtml",
            lang="ja",
        )
        series_item.content = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja">
<head>
  <meta charset="utf-8"/>
  <title>このシリーズの他の作品</title>
  <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
{series_html}
</body>
</html>""".encode("utf-8")
        series_item.add_item(css)
        book.add_item(series_item)
        epub_chapters.append(series_item)
        chapters = list(chapters) + [{"title": "このシリーズの他の作品"}]

    book.toc = [(epub.Section(ch["title"]), [item]) for ch, item in zip(chapters, epub_chapters)]
    book.spine = ["nav"] + epub_chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    timestamp = datetime.now(tz=JST).strftime("%Y%m%d_%H%M%S")
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)[:40]
    output_path = output_dir / f"{timestamp}_{safe_title}.epub"
    epub.write_epub(str(output_path), book)
    logging.info(f"epub生成完了: {output_path}")
    return output_path


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("formatter.py: ライブラリ動作確認")
    for lib, pkg in [("ebooklib", "ebooklib"), ("PIL", "Pillow"), ("fal_client", "fal-client"), ("requests", "requests")]:
        try:
            __import__(lib)
            print(f"✅ {pkg} OK")
        except ImportError:
            print(f"❌ {pkg} 未インストール → pip install {pkg}")
