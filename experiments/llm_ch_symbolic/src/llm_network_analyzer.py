"""Real-LLM network structure analysis for a NetworkIR."""

from __future__ import annotations

from pathlib import Path

from . import llm_client
from .network_ir_adapter import NetworkIR, topology_summary


def analyze_network(
    ir: NetworkIR,
    prompt_path: str | Path,
    config: llm_client.LLMConfig,
) -> dict:
    prompt = Path(prompt_path).read_text(encoding="utf-8")
    payload = topology_summary(ir)
    response = llm_client.call_chat(prompt, payload, config)
    return {
        "network_id": ir.network_id,
        "payload": payload,
        "prompt": prompt,
        "llm_response": response,
        "analysis": response["parsed"],
    }
