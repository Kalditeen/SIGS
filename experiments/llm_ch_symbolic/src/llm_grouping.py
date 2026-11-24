"""Orchestrate one real LLM grouping call using the fixed prompt file."""

from __future__ import annotations

from pathlib import Path

from . import llm_client, term_serializer


def run_llm_grouping(
    prompt_path: str | Path,
    residual_formal,
    config: llm_client.LLMConfig,
) -> dict:
    prompt = Path(prompt_path).read_text(encoding="utf-8")
    payload = term_serializer.serialize_terms(residual_formal)
    response = llm_client.call_chat(prompt, payload, config)
    return {
        "prompt": prompt,
        "serialized_terms": payload,
        "llm_response": response,
        "grouping": response["parsed"],
    }
