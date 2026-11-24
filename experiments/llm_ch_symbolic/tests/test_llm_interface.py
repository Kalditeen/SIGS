"""LLM config and request building tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.llm_client import (  # noqa: E402
    LLMNotConfiguredError,
    build_chat_request,
    load_config,
    redacted_config,
    LLMConfig,
)


def test_missing_key_is_reported(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    config = load_config(tmp_path / "missing.json")
    assert config.is_configured is False
    with pytest.raises(LLMNotConfiguredError):
        from src.llm_client import call_chat

        call_chat("prompt", {"terms": []}, config)


def test_request_does_not_contain_api_key() -> None:
    config = LLMConfig("https://api.deepseek.com", "secret-key", "deepseek-chat")
    request = build_chat_request("prompt", {"terms": []}, config)
    assert "secret-key" not in str(request)
    assert "Authorization" not in request
    assert request["temperature"] == 0


def test_redacted_config_never_exposes_key() -> None:

    config = LLMConfig("https://api.deepseek.com", "secret", "deepseek-chat")
    summary = redacted_config(config)
    assert summary["api_key_configured"] is True
    assert "api_key" not in summary
