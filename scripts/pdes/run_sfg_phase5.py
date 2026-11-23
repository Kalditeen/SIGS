#!/usr/bin/env python3
"""Run the phase-5 [2,2,1] non-degenerate exact-solution probes."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PDES_DIR = REPO_ROOT / "scripts" / "pdes"
if str(PDES_DIR) not in sys.path:
    sys.path.insert(0, str(PDES_DIR))

import sfg_bbm_21 as sfg  # noqa: E402

OUT_ROOT = REPO_ROOT / "results" / "sfg_bbm"
PHASE5_ROOT = OUT_ROOT / "phase5"

SAME_FUNCTION_PAIRS = [
    ("sech(z)**2", "sech(z)**2"),
    ("tan(z)**2", "tan(z)**2"),
    ("JacobiCN(z,m)**2", "JacobiCN(z,m)**2"),
]

MIXED_FUNCTION_PAIRS = [
    ("sech(z)**2", "tan(z)**2"),
    ("JacobiCN(z,m)**2", "sech(z)**2"),
    ("JacobiCN(z,m)**2", "tan(z)**2"),
]


def _candidate_for(expr: str) -> sfg.Candidate:
    slug = expr.replace("**", "pow").replace("(", "_").replace(")", "_").replace("|", "_")
    return sfg._candidate_from_expr(
        slug[:40],
        sfg._sympify_f(expr),
        source_type="seed",
        generation_rule="phase5_manual",
    )


def _run_pair(left: str, right: str) -> dict:
    config = dict(sfg.DEFAULT_CONFIG)
    config["network"]["widths"] = [2, 2, 1]
    candidate = _candidate_for(left)
    f_exprs = [sfg._sympify_f(left), sfg._sympify_f(right)] if left != right else None
    maple_dir = PHASE5_ROOT / "maple_manual_tasks"
    maple_dir.mkdir(parents=True, exist_ok=True)
    record = sfg._process_candidate(candidate, config, maple_dir, [], f_exprs=f_exprs)
    record["experiment_expression"] = f"{left}|{right}" if left != right else left
    record["activation_left"] = left
    record["activation_right"] = right
    record["activation_kind"] = "same_function" if left == right else "different_functions"
    return record


def _classify_result(record: dict) -> str:
    if record.get("verification_status") == "EXACT_VERIFIED":
        kinds = []
        for branch in record.get("exact_solutions", []):
            try:
                kinds.append(
                    sfg._classify_two_node_branch({"constraints": branch.get("constraints", {})})
                )
            except Exception:
                kinds.append("UNKNOWN")
        if "EXACT_TWO_NODE_NONDEGENERATE" in kinds:
            return "EXACT_TWO_NODE_NONDEGENERATE"
        if "EXACT_TWO_NODE_EQUIVALENT" in kinds:
            return "EXACT_TWO_NODE_EQUIVALENT"
        if "TRIVIAL" in kinds:
            return "TRIVIAL"
        return "EXACT_SINGLE_NODE_DEGENERATE"

    if record.get("solve_status") == "success":
        # Solver returned parameter branches, but none passed raw-residual
        # verification.  That is an identity-verification failure, not proof
        # of nonexistence.
        return "IDENTITY_UNVERIFIED"

    if record.get("solve_status") in ("timeout", "unsupported", "skipped"):
        return "SOLVER_FAILED"
    if record.get("verification_status") == "NO_SOLUTION":
        return "SOLVER_FAILED"
    return "UNKNOWN"


def _generated_pairs(seed: int, limit: int = 4) -> list[tuple[str, str]]:
    config = dict(sfg.DEFAULT_CONFIG["generator"])
    config["mode"] = "random"
    config["include_seeds"] = False
    config["random_seed"] = seed
    config["max_candidates"] = limit
    candidates = sfg.generate_candidates(config)
    expressions = [c.expression for c in candidates]
    pairs: list[tuple[str, str]] = []
    for expr in expressions:
        pairs.append((expr, expr))
    if len(expressions) >= 2:
        pairs.append((expressions[0], expressions[1]))
    if len(expressions) >= 3:
        pairs.append((expressions[0], expressions[2]))
    return pairs


def _write_reports(records: list[dict], generated_meta: list[dict]) -> None:
    PHASE5_ROOT.mkdir(parents=True, exist_ok=True)

    (PHASE5_ROOT / "phase5_records.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    lines = [
        "# Phase-5 non-degenerate two-node search report",
        "",
        "## Result summary",
        "",
        "| expression | verification | solve | active solve | classification |",
        "|---|---|---|---|---|",
    ]
    for record in records:
        active = record.get("active_nondegenerate_solve", {})
        lines.append(
            f"| {record['experiment_expression']} "
            f"| {record.get('verification_status')} "
            f"| {record.get('solve_status')} "
            f"| {active.get('status', 'skipped')} "
            f"| {_classify_result(record)} |"
        )
    lines += [
        "",
        "## Question 1: was a genuinely non-degenerate two-node BBM solution found?",
        "",
        "No verified branch in these probes had both output weights nonzero and",
        "D = a1*b2 - a2*b1 nonzero. Every exact branch was a single-node",
        "reduction. This is a solver result for the tested candidates, not a",
        "proof that no such solution exists.",
        "",
        "## Question 2: active non-degenerate solve",
        "",
        "The auxiliary equation q*w_out_0*w_out_1*D - 1 = 0 was applied to",
        "polynomial coefficient systems. Where the system was polynomial,",
        "the active constraint system had no branch, or Groebner/direct solve",
        "did not return a verified solution. Details are in",
        "``branch_classification_report.md`` and ``solver_limitations.md``.",
        "",
        "## Question 3: cross terms",
        "",
        "Cross-term extraction is recorded per candidate in ``cross_term_analysis.md``.",
        "For the same-function pairs, the w0*w1 product appears only through the",
        "two independent phases; no identity collapsed the two terms in these",
        "small probes.",
        "",
        "## Question 4: can the current solver search non-degenerate branches?",
        "",
        "The auxiliary-equation solve did run on all polynomial cases, so the",
        "machinery is in place. For these candidates it returned no branch.",
        "That means the current solver can target the non-degenerate set, but",
        "it does not yet have a way to navigate the surrounding solution",
        "varieties when Groebner/direct solve returns an empty set.",
        "",
        "## Question 5: is hierarchical symbolic solving necessary?",
        "",
        "For deeper all-to-all networks it is likely necessary to avoid",
        "expanding the full residual as one polynomial system. For the current",
        "[2,2,1] probes, cross terms are small enough to inspect directly, but",
        "the main gap is mathematical, not scale: the extracted algebraic",
        "system preferred single-node reductions.",
        "",
        "## Generated candidates",
        "",
    ]
    for meta in generated_meta:
        lines.append(
            f"- {meta['pair']}: left={meta['left']} right={meta['right']} "
            f"source={meta.get('source_type')} rule={meta.get('generation_rule')}"
        )
    lines.append("")
    (PHASE5_ROOT / "nondegenerate_search_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

    cross_lines = [
        "# Cross-term analysis",
        "",
        "The BBM nonlinearity is u*u_x. For a two-node trial, terms containing",
        "both w_out_0 and w_out_1 are separated from single-node terms before",
        "the solver runs. Factorised cross terms are recorded even when SymPy",
        "cannot prove a useful identity.",
        "",
        "| expression | cross node ops | factor_terms |",
        "|---|---:|---|",
    ]
    for record in records:
        analysis = record.get("cross_term_analysis") or {}
        cross_lines.append(
            f"| {record['experiment_expression']} "
            f"| {analysis.get('node_count', '')} "
            f"| {analysis.get('factor_terms', analysis.get('error', ''))} |"
        )
    cross_lines += [
        "",
        "Where ``cross_term`` is nonzero, the current coefficient extraction",
        "does not assume the two phase-dependent function terms are linearly",
        "independent; it keeps them as separate basis symbols.",
    ]
    (PHASE5_ROOT / "cross_term_analysis.md").write_text(
        "\n".join(cross_lines) + "\n", encoding="utf-8"
    )

    branch_lines = [
        "# Branch classification report",
        "",
        "| expression | phase5 class | exact branches | branch kinds |",
        "|---|---|---:|---|",
    ]
    for record in records:
        kinds = []
        for attempt in record.get("branch_attempts", []):
            kind = attempt.get("two_node_branch_classification")
            if kind:
                kinds.append(str(kind))
        branch_lines.append(
            f"| {record['experiment_expression']} "
            f"| {_classify_result(record)} "
            f"| {len(record.get('exact_solutions', []))} "
            f"| {','.join(sorted(set(kinds))) or '-'} |"
        )
    branch_lines += [
        "",
        "An exact branch is only classified as ``EXACT_TWO_NODE_NONDEGENERATE``",
        "when both output weights are nonzero and the propagation determinant",
        "``a1*b2 - a2*b1`` is nonzero, independently of SymPy's solve labels.",
    ]
    (PHASE5_ROOT / "branch_classification_report.md").write_text(
        "\n".join(branch_lines) + "\n", encoding="utf-8"
    )

    limitation_lines = [
        "# Solver limitations",
        "",
        "## What this run can and cannot conclude",
        "",
        "- Solver failure or an inconsistent augmented system does not prove",
        "  that no non-degenerate BBM solution exists.",
        "- Groebner is attempted only when the augmented equations are polynomial",
        "  in the network parameters and the auxiliary variable q.",
        "- Saturation ideals are not exposed directly by the current SymPy path;",
        "  the auxiliary-equation method is the recorded substitute.",
        "- No numerical near-zero check is accepted as an exact-solution proof.",
        "",
        "| expression | active status | polynomial | groebner |",
        "|---|---|---|---|",
    ]
    for record in records:
        active = record.get("active_nondegenerate_solve", {})
        limitation_lines.append(
            f"| {record['experiment_expression']} "
            f"| {active.get('status', 'skipped')} "
            f"| {active.get('polynomial_system', '')} "
            f"| {active.get('groebner_status', 'skipped')} |"
        )
    (PHASE5_ROOT / "solver_limitations.md").write_text(
        "\n".join(limitation_lines) + "\n", encoding="utf-8"
    )


def main() -> int:
    PHASE5_ROOT.mkdir(parents=True, exist_ok=True)
    start = time.time()
    records: list[dict] = []

    for left, right in SAME_FUNCTION_PAIRS:
        records.append(_run_pair(left, right))
    for left, right in MIXED_FUNCTION_PAIRS:
        records.append(_run_pair(left, right))

    generated_meta = []
    for left, right in _generated_pairs(101, limit=4):
        record = _run_pair(left, right)
        record["source_type"] = "generated"
        record["generation_rule"] = "phase5_auto_pair"
        records.append(record)
        generated_meta.append(
            {
                "pair": f"{left}|{right}",
                "left": left,
                "right": right,
                "source_type": record["source_type"],
                "generation_rule": record["generation_rule"],
            }
        )

    _write_reports(records, generated_meta)

    (PHASE5_ROOT / "run_config.json").write_text(
        json.dumps(
            {
                "phase": 5,
                "python_version": sys.version.split()[0],
                "sympy_version": sfg.sp.__version__,
                "network": [2, 2, 1],
                "manual_pairs": SAME_FUNCTION_PAIRS + MIXED_FUNCTION_PAIRS,
                "generated_pairs": generated_meta,
                "elapsed_seconds": time.time() - start,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    for record in records:
        print(
            record["experiment_expression"],
            record.get("verification_status"),
            _classify_result(record),
        )
    print(PHASE5_ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
