"""
agents/utils.py — KDPパイプライン共通ユーティリティ

- api_call_with_retry : 指数的バックオフによるAPIリトライ
- parse_json_response : LLMレスポンスからJSONを抽出・切断修復してパース
- call_claude         : retry + Geminiフォールバック付きClaude呼び出し
"""

from __future__ import annotations

import json
import logging
import random
import re
import time
from typing import Any, Callable, Optional


# ---------------------------------------------------------------------------
# 1. 指数的バックオフ（Exponential Backoff）
# ---------------------------------------------------------------------------

def api_call_with_retry(
    func: Callable,
    *args: Any,
    max_retries: int = 3,
    base_delay: float = 3.0,
    multiplier: float = 1.5,
    **kwargs: Any,
) -> Any:
    """
    指数的バックオフでAPIを呼び出す。
    429 / 500 / 503 / overloaded / rate_limit のみリトライ対象。
    """
    last_exc: Optional[Exception] = None
    for attempt in range(max_retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exc = e
            err = str(e).lower()
            retryable = any(
                code in err for code in
                ["429", "500", "503", "overload", "rate_limit", "too_many_requests"]
            )
            if retryable and attempt < max_retries:
                delay = base_delay * (multiplier ** attempt) + random.uniform(0.0, 1.0)
                logging.warning(
                    f"APIエラー (試行{attempt + 1}/{max_retries + 1}): {e}. "
                    f"{delay:.1f}秒後にリトライ..."
                )
                time.sleep(delay)
                continue
            break
    raise last_exc  # type: ignore[misc]


# ---------------------------------------------------------------------------
# 2. JSON切断修復 + パース
# ---------------------------------------------------------------------------

def _fix_truncated_json(raw: str) -> str:
    """max_tokens に達して途中切断されたJSONを補完する。"""
    raw = raw.strip()
    # 末尾の不完全なカンマを除去
    raw = re.sub(r",\s*$", "", raw)
    # 引用符が奇数なら閉じる
    if raw.count('"') % 2 != 0:
        raw += '"'
    # 括弧バランスを補完（] → } の順）
    open_brackets = raw.count("[") - raw.count("]")
    open_braces = raw.count("{") - raw.count("}")
    raw += "]" * max(0, open_brackets)
    raw += "}" * max(0, open_braces)
    return raw


def parse_json_response(text: str) -> Optional[dict]:
    """
    LLMレスポンステキストからJSONを抽出してパースする。
    1. コードブロック（```json ... ```）を優先
    2. 先頭の { ... } を探す
    3. パース失敗時は切断修復を試みる
    """
    # コードブロック内を優先
    code_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    raw = code_match.group(1) if code_match else None

    if not raw:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        raw = match.group() if match else None

    if not raw:
        logging.error("レスポンスにJSONが見つかりません")
        return None

    # trailing comma 除去
    raw = re.sub(r",\s*([}\]])", r"\1", raw)

    # 1回目: そのままパース
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # 2回目: 切断修復してパース
    fixed = _fix_truncated_json(raw)
    try:
        result = json.loads(fixed)
        logging.warning("JSONを自動修復してパースしました（切断検出）")
        return result
    except json.JSONDecodeError as e:
        logging.error(f"JSON修復失敗: {e}")
        return None


# ---------------------------------------------------------------------------
# 3. Claude呼び出し（retry + Gemini フォールバック）
# ---------------------------------------------------------------------------

def call_claude(
    client: Any,
    prompt: str,
    model: str = "claude-haiku-4-5-20251001",
    max_tokens: int = 4096,
    gemini_key: str = "",
) -> Optional[str]:
    """
    Claude APIを呼び出す。
    - 自動リトライ（Exponential Backoff）
    - Overloaded / RateLimit 時に gemini_key があれば Gemini Flash へフォールバック
    """
    def _anthropic_call() -> str:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return next((b.text for b in response.content if b.type == "text"), "")

    try:
        return api_call_with_retry(_anthropic_call)
    except Exception as e:
        err = str(e).lower()
        if gemini_key and any(
            code in err for code in ["429", "overload", "rate_limit", "too_many"]
        ):
            logging.warning(f"Anthropic Overloaded → Gemini Flash にフォールバック: {e}")
            return _call_gemini(prompt, gemini_key)
        raise


def _call_gemini(prompt: str, gemini_key: str) -> Optional[str]:
    """Gemini Flash（無料枠）でテキスト生成する。"""
    try:
        import google.generativeai as genai  # type: ignore[import]
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        text = response.text
        logging.info("Gemini Flash フォールバック成功")
        return text
    except ImportError:
        logging.error(
            "google-generativeai が未インストールです。"
            "pip install google-generativeai を実行してください。"
        )
        return None
    except Exception as e:
        logging.error(f"Gemini フォールバック失敗: {e}")
        return None
