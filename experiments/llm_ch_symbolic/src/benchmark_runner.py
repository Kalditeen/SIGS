"""Run a Phase 1.5 benchmark level and persist every result."""

from __future__ import annotations

import json
import time
from pathlib import Path

from . import benchmark_generator, llm_client, network_ir_adapter
from . import llm_network_analyzer, llm_strategy_planner
from . import strategy_validator, symbolic_executor, evaluation_metrics

METHODS = ("traditional", "manual", "llm", "all")

DEFAULT_PROMPTS = Path(__file__).resolve().parents[1] / "prompts"


def _write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )


def _run_llm_once(ir: network_ir_adapter.NetworkIR, config: llm_client.LLMConfig, output_dir: Path, repeat: int) -> dict:
    analysis_path = output_dir / f"analysis_llm_response_{repeat}.json"
    strategy_path = output_dir / f"strategy_llm_response_{repeat}.json"

    analysis_result = llm_network_analyzer.analyze_network(
        ir,
        DEFAULT_PROMPTS / "network_analysis_prompt.txt",
        config,
    )
    _write_json(analysis_path, {
        "request": analysis_result["llm_response"].get("request"),
        "raw_responses": analysis_result["llm_response"].get("raw_responses"),
        "parsed": analysis_result["llm_response"].get("parsed"),
        "parse_error": analysis_result["llm_response"].get("parse_error"),
        "model": analysis_result["llm_response"].get("model"),
        "timestamp_utc": analysis_result["llm_response"].get("timestamp_utc"),
    })

    analysis_validation = strategy_validator.validate_analysis(ir, analysis_result["analysis"])
    metrics = evaluation_metrics.evaluate_structure_recognition(ir, analysis_validation)

    if not analysis_validation["ok"]:
        return {
            "repeat": repeat,
            "analysis": analysis_result["analysis"],
            "analysis_validation": analysis_validation,
            "structure_metrics": metrics,
            "strategy_validation": None,
            "execution": None,
            "status": "analysis_invalid",
        }

    strategy_result = llm_strategy_planner.plan_strategy(
        ir.network_id,
        analysis_validation["normalized"],
        DEFAULT_PROMPTS / "symbolic_strategy_prompt.txt",
        config,
    )
    _write_json(strategy_path, {
        "request": strategy_result["llm_response"].get("request"),
        "raw_responses": strategy_result["llm_response"].get("raw_responses"),
        "parsed": strategy_result["llm_response"].get("parsed"),
        "parse_error": strategy_result["llm_response"].get("parse_error"),
        "model": strategy_result["llm_response"].get("model"),
        "timestamp_utc": strategy_result["llm_response"].get("timestamp_utc"),
    })

    strategy_validation = strategy_validator.validate_strategy(
        ir,
        analysis_validation["normalized"],
        strategy_result["strategy"],
    )
    if not strategy_validation["ok"]:
        return {
            "repeat": repeat,
            "analysis": analysis_result["analysis"],
            "analysis_validation": analysis_validation,
            "structure_metrics": metrics,
            "strategy": strategy_result["strategy"],
            "strategy_validation": strategy_validation,
            "execution": None,
            "status": "strategy_invalid",
        }

    execution = symbolic_executor.execute_strategy(ir, strategy_validation["normalized"])
    return {
        "repeat": repeat,
        "analysis": analysis_result["analysis"],
        "analysis_validation": analysis_validation,
        "structure_metrics": metrics,
        "strategy": strategy_result["strategy"],
        "strategy_validation": strategy_validation,
        "execution": execution,
        "status": "completed",
    }


def run_benchmarks(
    level: int | str,
    method: str = "all",
    repeat: int = 3,
    config: llm_client.LLMConfig | None = None,
    output_root: Path | None = None,
) -> dict:
    if method not in METHODS:
        raise ValueError(f"unknown method {method!r}; choose from {METHODS}")

    output_root = output_root or (
        Path(__file__).resolve().parents[1] / "results" / "phase15"
    )
    level_output = output_root / f"level{level}"
    cases = benchmark_generator.generate_benchmarks(level)

    stats = {
        "level": int(level),
        "method": method,
        "repeat": repeat,
        "case_count": len(cases),
        "traditional": [],
        "manual": [],
        "llm": [],
        "llm_repeat_results": [],
    }

    for ir in cases:
        case_dir = level_output / "cases" / ir.network_id
        _write_json(case_dir / "network_ir.json", ir.to_dict())

        traditional_result = symbolic_executor.execute_traditional(ir)
        manual_result = symbolic_executor.execute_manual(ir)
        _write_json(case_dir / "traditional_result.json", traditional_result)
        _write_json(case_dir / "manual_result.json", manual_result)
        stats["traditional"].append({
            "network_id": ir.network_id,
            "compile_status": traditional_result.get("compile_status"),
            "residual_terms": traditional_result.get("residual_terms"),
            "common_groups": traditional_result.get("common_term_grouping", {}).get("group_count"),
        })
        stats["manual"].append({
            "network_id": ir.network_id,
            "compile_status": manual_result.get("compile_status"),
            "residual_terms": manual_result.get("residual_terms"),
            "common_groups": manual_result.get("common_term_grouping", {}).get("group_count"),
        })

        llm_repeats = []
        if method in ("llm", "all"):
            if config is None or not config.is_configured:
                raise llm_client.LLMNotConfiguredError(
                    "LLM_API_NOT_CONFIGURED for llm/all methods"
                )
            for repeat_index in range(1, repeat + 1):
                llm_repeats.append(
                    _run_llm_once(ir, config, case_dir, repeat_index)
                )
        _write_json(case_dir / "llm_repeats.json", llm_repeats)
        stats["llm_repeat_results"].append({
            "network_id": ir.network_id,
            "repeats": llm_repeats,
        })
        stats["llm"].append({
            "network_id": ir.network_id,
            "repeat_count": len(llm_repeats),
            "analysis_ok": sum(1 for item in llm_repeats if item["status"] != "analysis_invalid"),
            "strategy_ok": sum(1 for item in llm_repeats if item.get("strategy_validation", {}).get("ok")),
            "execution_ok": sum(1 for item in llm_repeats if item.get("execution") and item["execution"].get("compile_status") == "success"),
        })

    _write_json(level_output / "run_config.json", {
        "level": int(level),
        "method": method,
        "repeat": repeat,
        "case_count": len(cases),
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    })
    _write_json(level_output / "statistics.json", stats)
    return stats
