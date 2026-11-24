"""OpenAI-compatible HTTP client for the DeepSeek API.

API keys are only read from environment variables or a local config file.
They are never written to source, logs, requests, or result files.
"""

from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


class LLMNotConfiguredError(RuntimeError):
    """Raised when no API key can be loaded."""


@dataclass
class LLMConfig:
    api_base: str
    api_key: str
    model: str
    temperature: float = 0.0
    timeout_seconds: float = 120.0
    max_retries: int = 3
    verify_tls: bool = True

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key.strip())


def load_config(path: str | Path | None = None) -> LLMConfig:
    """Load config from env, then merge a local JSON file if present.

    Precedence: environment variables override file values.  Supported env
    names are ``LLM_API_KEY``/``DEEPSEEK_API_KEY``,
    ``LLM_BASE_URL``/``DEEPSEEK_BASE_URL``, and ``LLM_MODEL``.
    """
    defaults: dict = {
        "api_base": "https://api.deepseek.com",
        "api_key": "",
        "model": "deepseek-chat",
        "temperature": 0.0,
        "timeout_seconds": 120.0,
        "max_retries": 3,
        "verify_tls": True,
    }

    if path is not None:
        config_path = Path(path)
        if config_path.exists():
            data = json.loads(config_path.read_text(encoding="utf-8"))
            defaults.update({key: value for key, value in data.items() if value is not None})

    api_key = os.environ.get("LLM_API_KEY") or os.environ.get("DEEPSEEK_API_KEY") or defaults["api_key"]
    api_base = os.environ.get("LLM_BASE_URL") or os.environ.get("DEEPSEEK_BASE_URL") or defaults["api_base"]
    model = os.environ.get("LLM_MODEL") or defaults["model"]

    return LLMConfig(
        api_base=str(api_base).rstrip("/"),
        api_key=str(api_key),
        model=str(model),
        temperature=float(defaults["temperature"]),
        timeout_seconds=float(defaults["timeout_seconds"]),
        max_retries=int(defaults["max_retries"]),
        verify_tls=bool(defaults["verify_tls"]),
    )


def redacted_config(config: LLMConfig) -> dict:
    return {
        "api_base": config.api_base,
        "api_key_configured": config.is_configured,
        "model": config.model,
        "temperature": config.temperature,
        "timeout_seconds": config.timeout_seconds,
        "max_retries": config.max_retries,
        "verify_tls": config.verify_tls,
    }


def build_chat_request(prompt: str, payload: dict, config: LLMConfig) -> dict:
    """Build an OpenAI-compatible chat request. No key is included here."""
    content = prompt + "\n\n" + json.dumps(payload, ensure_ascii=False, indent=2)
    return {
        "model": config.model,
        "temperature": config.temperature,
        "messages": [{"role": "user", "content": content}],
    }


def _extract_json(text: str):
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Fall back to the outermost JSON object if the model wrapped it in prose.
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        return json.loads(text[start : end + 1])
    raise ValueError("response contains no parseable JSON object")


def _post_once(url: str, request: dict, config: LLMConfig) -> str:
    body = json.dumps(request).encode("utf-8")
    http_request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.api_key}",
        },
        method="POST",
    )
    if config.verify_tls:
        ssl_context = ssl.create_default_context()
        try:
            import certifi

            ssl_context.load_verify_locations(certifi.where())
        except Exception:  # noqa: BLE001 - fall back to system trust store
            pass
    else:
        ssl_context = ssl._create_unverified_context()
    with urllib.request.urlopen(
        http_request, timeout=config.timeout_seconds, context=ssl_context
    ) as response:
        return response.read().decode("utf-8")


def call_chat(
    prompt: str,
    payload: dict,
    config: LLMConfig,
    correction_message: str = (
        "你的上一轮回复不是合法 JSON。请只输出一个 JSON 对象，不要包含 Markdown、"
        "代码围栏或解释文字。"
    ),
) -> dict:
    """Call the API and return raw responses plus the parsed grouping JSON."""
    if not config.is_configured:
        raise LLMNotConfiguredError(
            "LLM_API_NOT_CONFIGURED: set LLM_API_KEY or DEEPSEEK_API_KEY, "
            "or fill api_key in config/llm_config.json"
        )

    url = config.api_base.rstrip("/") + "/chat/completions"
    request = build_chat_request(prompt, payload, config)
    raw_responses: list[str] = []
    parsed = None
    last_error: str | None = None

    for attempt in range(config.max_retries):
        try:
            raw = _post_once(url, request, config)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            last_error = f"HTTP {exc.code}: {detail[:1000]}"
            raw_responses.append(last_error)
            break
        except urllib.error.URLError as exc:
            last_error = f"URL error: {exc.reason}"
            raw_responses.append(last_error)
            break
        except Exception as exc:  # noqa: BLE001 - report transport failures verbatim
            last_error = f"{type(exc).__name__}: {exc}"
            raw_responses.append(last_error)
            break

        raw_responses.append(raw)
        try:
            payload_text = json.loads(raw)["choices"][0]["message"]["content"]
        except Exception as exc:  # noqa: BLE001
            payload_text = raw

        try:
            parsed = _extract_json(payload_text)
            break
        except Exception as exc:  # noqa: BLE001
            last_error = f"JSON parse failed: {type(exc).__name__}: {exc}"
            if attempt + 1 < config.max_retries:
                request["messages"].append({"role": "assistant", "content": payload_text})
                request["messages"].append({"role": "user", "content": correction_message})

    return {
        "model": config.model,
        "temperature": config.temperature,
        "url": url,
        "request": request,
        "raw_responses": raw_responses,
        "parsed": parsed,
        "parse_error": None if parsed is not None else last_error,
        "attempts": len(raw_responses),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
