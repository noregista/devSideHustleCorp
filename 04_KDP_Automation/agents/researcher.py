"""
agents/researcher.py

日本語トレンドRSSを取得し、実データをもとにKDP向けテーマを生成する。
（旧: Claude の学習データだけで生成 → 新: 実際のトレンド記事を食わせて生成）

使用モデル: claude-haiku-4-5（コスト最小化）
"""

from __future__ import annotations

import json
import logging
import os
import re
import socket
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import email.utils
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import anthropic as _anthropic_module
    _client: Optional[Any] = (
        _anthropic_module.Anthropic() if os.environ.get("ANTHROPIC_API_KEY") else None
    )
except ImportError:
    _client = None

socket.setdefaulttimeout(15)

BASE_DIR = Path(__file__).parent.parent
RESEARCH_CACHE_DIR = BASE_DIR / "research_cache"
LOG_PATH = BASE_DIR / "logs" / "researcher.log"
JST = timezone(timedelta(hours=9))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# トレンド収集に使うRSSソース（ジャンル別）
RSS_SOURCES = [
    # ビジネス・マネー
    "https://toyokeizai.net/list/feed/rss",
    "https://diamond.jp/list/feed/rss",
    # テクノロジー・AI
    "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",
    "https://rss.itmedia.co.jp/rss/2.0/itmediabusiness.xml",
    # ライフスタイル・健康
    "https://news.yahoo.co.jp/rss/topics/life.xml",
    # 総合ニュース
    "https://news.yahoo.co.jp/rss/topics/top-picks.xml",
]

MAX_ARTICLES_PER_SOURCE = 10  # 1ソースあたり最大取得件数
MAX_TOTAL_ARTICLES = 40       # Claudeに渡す記事数の上限


def setup_file_logging() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logging.getLogger().addHandler(handler)


def save_json(path: Path, data: Any) -> None:
    tmp = path.with_suffix(".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        tmp.replace(path)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise


def fetch_rss(url: str, timeout: int = 10) -> Optional[str]:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "KDPResearcher/1.0"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        logging.warning(f"RSS取得失敗 [{url}]: {e}")
        return None


def parse_rss_titles(xml_text: str) -> list[str]:
    """RSSからタイトルだけ抽出して返す。"""
    titles = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return titles
    for item in root.findall(".//item"):
        title_el = item.find("title")
        if title_el is not None and title_el.text:
            titles.append(title_el.text.strip())
    return titles


def collect_trending_titles(max_total: int = MAX_TOTAL_ARTICLES) -> list[str]:
    """複数RSSから並列でタイトルを収集する。"""
    all_titles: list[str] = []

    def _fetch(url: str) -> list[str]:
        xml = fetch_rss(url)
        if not xml:
            return []
        titles = parse_rss_titles(xml)
        return titles[:MAX_ARTICLES_PER_SOURCE]

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(_fetch, url): url for url in RSS_SOURCES}
        for future in as_completed(futures, timeout=30):
            try:
                titles = future.result()
                all_titles.extend(titles)
                logging.info(f"  RSS取得: {futures[future]} → {len(titles)}件")
            except Exception as e:
                logging.warning(f"RSS並列取得エラー [{futures[future]}]: {e}")

    # 重複除去・上限カット
    seen = set()
    unique = []
    for t in all_titles:
        if t not in seen:
            seen.add(t)
            unique.append(t)
        if len(unique) >= max_total:
            break

    logging.info(f"トレンド記事タイトル収集完了: {len(unique)}件")
    return unique


RESEARCH_PROMPT = """
あなたはAmazon KDP（Kindle Direct Publishing）の日本語市場に精通した
出版コンサルタントです。

以下は現在（{date}）の日本のトレンドニュース・記事タイトルの一覧です。

【今日のトレンド記事タイトル（実データ）】
{trending_titles}

上記のトレンドを参考に、日本語Amazon KDPで売れやすい電子書籍のテーマを8つ提案してください。

【選定基準】
- 上記トレンドが示す現在の関心・悩みに応えるテーマを優先する
- 50〜100ページ程度の実用書・ハウツー本として成立する
- 競合が多すぎず、新規参入の余地がある
- 時流に乗っているが、数年間は需要が続く
- ジャンルは問わない（ビジネス・健康・趣味・人間関係・節約・AI活用など）

以下のJSON形式のみで返すこと：

{{
  "researched_at": "{date}",
  "trending_source_count": {source_count},
  "candidates": [
    {{
      "title": "本のタイトル案（具体的で魅力的なもの）",
      "subtitle": "サブタイトル案",
      "genre": "ジャンル（ビジネス/健康/趣味/人間関係/マネー/自己啓発/その他）",
      "target_reader": "ターゲット読者層（具体的に）",
      "core_problem": "この本が解決する読者の悩みや課題",
      "key_selling_point": "なぜこの本が売れるか（差別化ポイント）",
      "estimated_chapters": ["章タイトル1", "章タイトル2", "章タイトル3", "章タイトル4", "章タイトル5"],
      "market_timing": "今このテーマが売れやすい理由（トレンドとの関連を含む）"
    }}
  ]
}}
"""


def research_topics(trending_titles: list[str]) -> Optional[dict]:
    if _client is None:
        logging.error("ANTHROPIC_API_KEY が設定されていません")
        return None

    today = datetime.now(tz=JST).strftime("%Y-%m-%d")
    titles_text = "\n".join(f"- {t}" for t in trending_titles)
    prompt = RESEARCH_PROMPT.format(
        date=today,
        trending_titles=titles_text,
        source_count=len(trending_titles),
    )

    logging.info("KDPテーマ生成開始（実トレンドデータ使用）...")
    try:
        response = _client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        text = next((b.text for b in response.content if b.type == "text"), "")
        code_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        raw = code_match.group(1) if code_match else None
        if not raw:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            raw = match.group() if match else None
        if not raw:
            logging.error("レスポンスにJSONが見つかりません")
            return None
        raw = re.sub(r',\s*([}\]])', r'\1', raw)
        data = json.loads(raw)
        logging.info(f"テーマ生成完了: {len(data.get('candidates', []))}件の候補")
        return data
    except json.JSONDecodeError as e:
        logging.error(f"JSONパースエラー: {e}")
        return None
    except Exception as e:
        logging.error(f"リサーチ失敗: {e}")
        return None


def main() -> Optional[dict]:
    setup_file_logging()
    logging.info("=== researcher 開始 ===")

    # Step1: RSSからトレンドタイトルを収集
    logging.info("トレンドRSSを取得中...")
    trending_titles = collect_trending_titles()

    # RSSが取れなかった場合はフォールバック（旧来のClaudeだけ生成）
    if not trending_titles:
        logging.warning("トレンドデータ取得失敗。Claude学習データのみで生成します（フォールバック）")
        trending_titles = []

    # Step2: 実データをClaudeに食わせてテーマ生成
    result = research_topics(trending_titles)

    if result:
        today = datetime.now(tz=JST).strftime("%Y-%m-%d")
        RESEARCH_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_path = RESEARCH_CACHE_DIR / f"{today}.json"
        save_json(cache_path, result)
        logging.info(f"リサーチ結果を保存: {cache_path}")
    else:
        logging.warning("テーマ生成失敗")

    logging.info("=== researcher 完了 ===")
    return result


if __name__ == "__main__":
    main()
