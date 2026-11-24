"""Real-LLM symbolic strategy planning after network analysis."""

from __future__ import annotations

from pathlib import Path

from . import llm_client
from .symbolic_rule_registry import rule_catalog


def plan_strategy(
    network_id: str,
    analysis: dict,
    prompt_path: str | Path,
    config: llm_client.LLMConfig,
) -> dict:
    prompt = Path(prompt_path).read_text(encoding="utf-8")
    payload = {
        "network_id": network_id,
        "network_analysis": analysis,
        "available_rules": rule_catalog(),
    }
    response = llm_client.call_chat(prompt, payload, config)
    return {
        "network_id": network_id,
        "payload": payload,
        "prompt": prompt,
        "llm_response": response,
        "strategy": response["parsed"],
    }
