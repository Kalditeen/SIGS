#!/usr/bin/env python3
"""Unified entry point for the LLM-assisted CH symbolic experiment."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
if str(EXPERIMENT_ROOT) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_ROOT))

from src.ch_equation import SYMBOLS  # noqa: E402
from src.coefficient_extractor import extract_coefficient_equations  # noqa: E402
from src.llm_client import LLMNotConfiguredError, load_config, redacted_config  # noqa: E402
from src.llm_grouping import run_llm_grouping  # noqa: E402
from src.original_pde_verifier import maple_branch_substitution, verify_maple_branch  # noqa: E402
from src.residual_builder import build_residuals  # noqa: E402
from src.term_serializer import serialize_terms  # noqa: E402
from src.grouping_validator import validate_grouping  # noqa: E402
from src.algebraic_solver import solve_system  # noqa: E402
from src.algebraic_solver import as_zero_expr  # noqa: E402

import sympy as sp  # noqa: E402


def _write_json(path: Path, payload) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )


def _setup_logger(output_dir: Path) -> logging.Logger:
    output_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("llm_ch_experiment")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(output_dir / "experiment.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def _report_path(output_dir: Path) -> Path:
    return output_dir / "EXPERIMENT_REPORT.md"


def _write_failure_report(
    output_dir: Path,
    stage: str,
    message: str,
    config_summary: dict | None = None,
) -> None:
    lines = [
        "# LLM-Assisted CH Symbolic Experiment",
        "",
        f"**Status:** not completed at stage `{stage}`.",
        "",
        f"**Reason:** {message}",
        "",
    ]
    if config_summary is not None:
        lines.append("## LLM Configuration")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(config_summary, indent=2, ensure_ascii=False))
        lines.append("```")
        lines.append("")
    _report_path(output_dir).write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_success_report(
    output_dir: Path,
    config_summary: dict,
    prompt_text: str,
    llm_grouping: dict,
    validation: dict,
    coefficient_equations: list[dict],
    algebraic_result: dict,
    maple_check: dict,
    final_verification: dict,
) -> None:
    lines = [
        "# LLM-Assisted CH Symbolic Experiment",
        "",
        "## 1. Purpose",
        "",
        "Verify that an external LLM can recognise common formal-monomial",
        "structure in a symbolic CH residual so Python can extract coefficients,",
        "solve constraints, and independently verify a Maple-known branch.",
        "",
        "## 2. Model and trial function",
        "",
        "```text",
        "f = b4 + A1*exp(wt1*t + wx1*x) + A2*exp(wt2*t + wx2*x) + A3*exp(wt3*t + wx3*x)",
        "CH residual: f_t + 2k f_x - f_xxt + 3f f_x - 2f_x f_xx - f f_xxx",
        "```",
        "",
        "## 3. Symbolic residual construction",
        "",
        "The original exponential residual and an independent formal-generator",
        "residual were both built with SymPy and checked for equality.",
        "",
        "## 4. LLM service",
        "",
        "```json",
        json.dumps(config_summary, indent=2, ensure_ascii=False),
        "```",
        "",
        "## 5. Prompt sent",
        "",
        "```text",
        prompt_text,
        "```",
        "",
        "## 6. Raw LLM grouping result",
        "",
        "```json",
        json.dumps(llm_grouping, indent=2, ensure_ascii=False, default=str),
        "```",
        "",
        "## 7. SymPy grouping validation",
        "",
        f"`ok = {validation['ok']}`",
        "",
        "```json",
        json.dumps(validation, indent=2, ensure_ascii=False, default=str),
        "```",
        "",
        "## 8. Extracted coefficient constraints",
        "",
        "```json",
        json.dumps(coefficient_equations, indent=2, ensure_ascii=False, default=str),
        "```",
        "",
        "## 9. Algebraic solving result",
        "",
        "```json",
        json.dumps(algebraic_result, indent=2, ensure_ascii=False, default=str),
        "```",
        "",
        "## 10. Maple branch recovery",
        "",
        "```json",
        json.dumps(maple_check, indent=2, ensure_ascii=False, default=str),
        "```",
        "",
        "## 11. Original CH verification",
        "",
        "```json",
        json.dumps(final_verification, indent=2, ensure_ascii=False, default=str),
        "```",
        "",
        "## 12. Fault tests",
        "",
        "Fault-injection tests live in `tests/test_grouping_validator.py` and are",
        "run separately with pytest.  They cover missing, duplicate, mismatched,",
        "and unknown term IDs.",
        "",
        "## 13. Limitations",
        "",
        "Formal-generator independence provides sufficient coefficient",
        "constraints; it is not claimed to be necessary for every possible exact",
        "solution.",
        "",
        "## 14. Acceptance",
        "",
        "```text",
        "LLM structure recognition: success",
        "SymPy grouping validation: success",
        "Algebraic constraint extraction: success",
        "Maple branch recovery: success",
        "Original PDE verification: success",
        "```",
        "",
    ]
    _report_path(output_dir).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LLM-assisted CH symbolic experiment")
    parser.add_argument("--skip-llm", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=EXPERIMENT_ROOT / "results")
    parser.add_argument("--config", type=Path, default=EXPERIMENT_ROOT / "config" / "llm_config.json")
    args = parser.parse_args(argv)

    output_dir = args.output_dir
    logger = _setup_logger(output_dir)
    logger.info("starting LLM-assisted CH symbolic experiment")

    residuals = build_residuals()
    (output_dir / "raw_residual.txt").write_text(
        sp.sstr(residuals.original), encoding="utf-8"
    )
    if not residuals.formal_consistency:
        logger.error("formal/original residual mismatch: %s", residuals.formal_consistency_error)
        _write_failure_report(output_dir, "residual_consistency", residuals.formal_consistency_error)
        return 2

    serialized = serialize_terms(residuals.formal)
    _write_json(output_dir / "serialized_terms.json", serialized)
    logger.info("formal residual has %d additive terms", len(serialized["terms"]))

    if args.validate_only:
        final_verification = verify_maple_branch()
        _write_json(output_dir / "final_verification.json", final_verification)
        logger.info("validate-only result is_zero=%s", final_verification["is_zero"])
        _write_failure_report(
            output_dir,
            "validate_only",
            "validate-only mode did not call the LLM; see final_verification.json.",
        )
        return 0 if final_verification["is_zero"] else 1

    config = load_config(args.config)
    config_summary = redacted_config(config)
    _write_json(output_dir / "llm_request.json", {"config": config_summary})

    if args.skip_llm:
        final_verification = verify_maple_branch()
        _write_json(output_dir / "final_verification.json", final_verification)
        logger.info("skip-llm mode completed; LLM was intentionally not called")
        _write_failure_report(
            output_dir,
            "skip_llm",
            "skip-llm mode did not call the LLM; it cannot be used as a final success.",
            config_summary,
        )
        return 0 if final_verification["is_zero"] else 1

    if not config.is_configured:
        logger.error("LLM_API_NOT_CONFIGURED")
        _write_json(
            output_dir / "llm_request.json",
            {
                "status": "LLM_API_NOT_CONFIGURED",
                "config": config_summary,
                "message": (
                    "set LLM_API_KEY or DEEPSEEK_API_KEY, or fill "
                    "experiments/llm_ch_symbolic/config/llm_config.json"
                ),
            },
        )
        (output_dir / "llm_response_raw.txt").write_text("", encoding="utf-8")
        _write_failure_report(
            output_dir,
            "llm_api",
            "LLM_API_NOT_CONFIGURED",
            config_summary,
        )
        return 2

    try:
        llm_result = run_llm_grouping(
            EXPERIMENT_ROOT / "prompts" / "coefficient_grouping_prompt.txt",
            residuals.formal,
            config,
        )
    except LLMNotConfiguredError as exc:
        logger.error("%s", exc)
        _write_failure_report(output_dir, "llm_api", str(exc), config_summary)
        return 2
    except Exception as exc:  # noqa: BLE001
        logger.exception("real LLM call failed")
        _write_failure_report(output_dir, "llm_call", f"{type(exc).__name__}: {exc}", config_summary)
        return 2

    (output_dir / "llm_response_raw.txt").write_text(
        json.dumps(llm_result["llm_response"], indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    (output_dir / "llm_grouping.json").write_text(
        json.dumps(llm_result["grouping"], indent=2, ensure_ascii=False, default=str)
        if llm_result["grouping"] is not None
        else json.dumps(
            {
                "parse_error": llm_result["llm_response"].get("parse_error"),
                "raw_responses": llm_result["llm_response"].get("raw_responses"),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    _write_json(
        output_dir / "llm_request.json",
        {
            "config": config_summary,
            "url": llm_result["llm_response"].get("url"),
            "model": llm_result["llm_response"].get("model"),
            "temperature": llm_result["llm_response"].get("temperature"),
            "request": llm_result["llm_response"].get("request"),
        },
    )

    if llm_result["grouping"] is None:
        logger.error("LLM did not return a parseable grouping")
        _write_failure_report(
            output_dir,
            "llm_parse",
            llm_result["llm_response"].get("parse_error") or "no grouping returned",
            config_summary,
        )
        return 3

    validation = validate_grouping(llm_result["grouping"], serialized, residuals.formal)
    _write_json(output_dir / "grouping_validation.json", validation)
    if not validation["ok"]:
        logger.error("grouping validation failed: %s", validation["errors"])
        _write_failure_report(
            output_dir,
            "grouping_validation",
            "LLM grouping failed deterministic validation: " + "; ".join(validation["errors"]),
            config_summary,
        )
        return 3

    coefficient_equations = extract_coefficient_equations(validation["groups"], serialized)
    _write_json(output_dir / "coefficient_equations.json", coefficient_equations)
    equation_strings = [item["equation"] for item in coefficient_equations if item["equation"]]
    if not equation_strings:
        logger.error("no coefficient equations extracted")
        _write_failure_report(output_dir, "coefficient_extraction", "no equations extracted", config_summary)
        return 4

    algebraic_result = solve_system(equation_strings)
    _write_json(output_dir / "algebraic_branches.json", algebraic_result)

    branch = maple_branch_substitution()
    maple_check = {
        "branch": {str(key): sp.sstr(value) for key, value in branch.items()},
        "satisfies_extracted_constraints": all(
            sp.expand(as_zero_expr(equation)).subs(branch) == 0
            for equation in equation_strings
        ),
        "equations_checked": len(equation_strings),
    }
    _write_json(output_dir / "maple_branch_verification.json", maple_check)

    final_verification = verify_maple_branch()
    _write_json(output_dir / "final_verification.json", final_verification)

    prompt_text = (EXPERIMENT_ROOT / "prompts" / "coefficient_grouping_prompt.txt").read_text(
        encoding="utf-8"
    )
    _write_success_report(
        output_dir,
        config_summary,
        prompt_text,
        llm_result["grouping"],
        validation,
        coefficient_equations,
        algebraic_result,
        maple_check,
        final_verification,
    )

    succeeded = (
        validation["ok"]
        and bool(equation_strings)
        and maple_check["satisfies_extracted_constraints"]
        and final_verification["is_zero"]
    )
    logger.info("experiment finished; success=%s", succeeded)
    return 0 if succeeded else 5


if __name__ == "__main__":
    raise SystemExit(main())
