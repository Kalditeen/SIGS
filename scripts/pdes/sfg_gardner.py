#!/usr/bin/env python3
"""SFG + NNSCA exact-solution search for the Gardner equation.

This module reuses the SFG candidate generator, the NNSCA network builder,
constraint extraction, and raw-residual certification from
``sfg_bbm_21.py``.  The only PDE-specific pieces are the Gardner residual
and Gardner-specific audit/report helpers.

The primary Gardner form is

    u_t + alpha*u*u_x + beta*u**2*u_x + gamma*u_{xxx} = 0.

The first experiment fixes alpha=beta=gamma=1.  The coefficient parameters
remain configurable and are not written into the network or SFG modules.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
import time
from collections import Counter
from pathlib import Path

import sympy as sp

REPO_ROOT = Path(__file__).resolve().parents[2]
PDES_DIR = REPO_ROOT / "scripts" / "pdes"
if str(PDES_DIR) not in sys.path:
    sys.path.insert(0, str(PDES_DIR))

import sfg_bbm_21 as sfg  # noqa: E402
import sfg_reduction  # noqa: E402

DEFAULT_RESULTS_DIR = REPO_ROOT / "results" / "gardner"
GARDNER_PDE_STR = "gardner_equation=ut + u*ux + u**2*ux + uxxx = 0"


def gardner_residual(u: sp.Expr, alpha=1, beta=1, gamma=1) -> sp.Expr:
    """Raw Gardner residual with configurable coefficients.

    The cubic term is intentionally ``u**2 * u_x``.  Do not confuse it with
    ``u * (u_x)**2``.
    """
    return (
        sp.diff(u, sfg.T)
        + alpha * u * sp.diff(u, sfg.X)
        + beta * u**2 * sp.diff(u, sfg.X)
        + gamma * sp.diff(u, sfg.X, 3)
    )


def residual_fn_for(alpha=1, beta=1, gamma=1):
    """Return a one-argument residual callable for ``_process_candidate``."""
    return lambda u: gardner_residual(u, alpha=alpha, beta=beta, gamma=gamma)


def _coefficient_label(alpha, beta, gamma) -> str:
    return f"alpha={alpha}, beta={beta}, gamma={gamma}"


def _solution_notes(source_expression: str, constraints: dict[str, str]):
    """Gardner-specific domain and parameter notes.

    BBM's ``tan**2`` notes are similar, but this function lives in the
    Gardner module so future Gardner-specific restrictions can be added
    without touching BBM results.
    """
    conditions: list[str] = []
    notes: list[str] = []
    expression = str(source_expression)

    if "tan" in expression:
        conditions.append("a != 0")
        notes.append(
            "tan/tan**2 has poles where cos(phase)=0; the solution is valid "
            "only on intervals avoiding phase = pi/2 + k*pi."
        )
    if "sech" in expression:
        conditions.append("a != 0")
        notes.append("sech-based waves are smooth on the real axis.")
    if "Jacobi" in expression:
        conditions.append("m != 0 for a genuinely elliptic branch")
        conditions.append("parameter denominators must be nonzero")
        notes.append("The elliptic parameter is the modulus square m.")
    if not conditions:
        conditions.append("nonzero propagation coefficients required for a nonconstant wave")
    return conditions, notes


def audit_exact_solution(
    source_expression: str,
    constraints: dict[str, str],
    alpha=1,
    beta=1,
    gamma=1,
) -> dict:
    """Rebuild u=c0+c1*f(a*x+b*t+d) and verify the raw Gardner residual."""
    try:
        f_expr = sfg._sympify_f(source_expression)
        trial = sfg.C0 + sfg.C1 * f_expr.subs(
            sfg.Z, sfg.A * sfg.X + sfg.B * sfg.T + sfg.D
        )
    except Exception as exc:
        return {
            "source_expression": source_expression,
            "constraints": constraints,
            "status": "SYMBOLIC_UNRESOLVED",
            "residual": None,
            "error": f"trial construction failed: {type(exc).__name__}: {exc}",
        }

    subs = {}
    for key, value in constraints.items():
        try:
            subs[sp.Symbol(key)] = sp.sympify(value, locals=dict(sfg.SYMPY_LOCALS))
        except Exception as exc:
            return {
                "source_expression": source_expression,
                "constraints": constraints,
                "status": "SYMBOLIC_UNRESOLVED",
                "residual": None,
                "error": f"constraint parse failed: {exc}",
            }

    try:
        u_sub = sp.expand(trial.subs(subs))
        residual = sp.expand(gardner_residual(u_sub, alpha, beta, gamma))
    except Exception as exc:
        return {
            "source_expression": source_expression,
            "constraints": constraints,
            "status": "SYMBOLIC_UNRESOLVED",
            "residual": None,
            "error": f"residual computation failed: {type(exc).__name__}: {exc}",
        }

    certified = sfg._residual_is_zero(residual)
    conditions, notes = _solution_notes(source_expression, constraints)
    return {
        "source_expression": source_expression,
        "constraints": constraints,
        "trial_expression": sp.sstr(u_sub),
        "residual": sp.sstr(residual),
        "status": "EXACT_VERIFIED" if certified else "SYMBOLIC_UNRESOLVED",
        "certified_zero": certified,
        "parameter_conditions": conditions,
        "domain_notes": notes,
    }


def _audit_trial(
    trial: sp.Expr,
    constraints: dict[str, str],
    alpha=1,
    beta=1,
    gamma=1,
) -> dict:
    """Verify one already-built NNSCA trial with the raw Gardner residual."""
    subs = {}
    for key, value in constraints.items():
        try:
            subs[sp.Symbol(key)] = sp.sympify(value, locals=dict(sfg.SYMPY_LOCALS))
        except Exception as exc:
            return {
                "constraints": constraints,
                "status": "SYMBOLIC_UNRESOLVED",
                "residual": None,
                "error": f"constraint parse failed: {exc}",
            }
    try:
        u_sub = sp.expand(trial.subs(subs))
    except Exception as exc:
        return {
            "constraints": constraints,
            "status": "SYMBOLIC_UNRESOLVED",
            "residual": None,
            "error": f"substitution failed: {exc}",
        }
    try:
        residual = sp.expand(gardner_residual(u_sub, alpha, beta, gamma))
    except Exception as exc:
        return {
            "constraints": constraints,
            "status": "SYMBOLIC_UNRESOLVED",
            "residual": None,
            "error": f"residual computation failed: {type(exc).__name__}: {exc}",
        }
    certified = sfg._residual_is_zero(residual)
    return {
        "constraints": constraints,
        "trial_expression": sp.sstr(u_sub),
        "residual": sp.sstr(residual),
        "status": "EXACT_VERIFIED" if certified else "SYMBOLIC_UNRESOLVED",
        "certified_zero": certified,
        "parameter_conditions": [],
        "domain_notes": [],
    }


def _classify_gardner_result(record: dict) -> str:
    """Map a processed record to the Gardner status vocabulary."""
    status = record.get("verification_status")
    if status == "EXACT_VERIFIED":
        return "EXACT_VERIFIED"
    if status == "NO_SOLUTION":
        return "SOLVER_FAILED"
    if status == "SYMBOLIC_UNRESOLVED":
        return "UNSUPPORTED" if record.get("solve_status") in ("timeout", "unsupported") else "IDENTITY_UNVERIFIED"
    if status == "UNSUPPORTED":
        return "UNSUPPORTED"
    if record.get("solve_status") == "success":
        return "IDENTITY_UNVERIFIED"
    if status == "FAILED":
        return "IDENTITY_UNVERIFIED"
    return "UNKNOWN"


def _write_failure_analysis(results_dir: Path, processed: list[dict]) -> Path:
    solve_success_failed = [
        record
        for record in processed
        if record.get("solve_status") == "success"
        and record.get("verification_status") != "EXACT_VERIFIED"
    ]
    lines = [
        "# Gardner failure analysis",
        "",
        "A `solve_status=success` record means SymPy returned parameter",
        "branches for the extracted algebraic coefficient system. It does not",
        "mean the original Gardner residual is identically zero. Every branch",
        "is independently back-substituted below.",
        "",
    ]
    for record in solve_success_failed:
        lines.append(f"## {record['function_id']}: {record['expression']}")
        lines.append(f"- symbolic_status: {record.get('symbolic_status')}")
        lines.append(f"- constraint_status: {record.get('constraint_status')}")
        lines.append(f"- solve_status: {record.get('solve_status')}")
        lines.append(f"- nontrivial_status: {record.get('nontrivial_status')}")
        lines.append(f"- substitution_status: {record.get('substitution_status')}")
        lines.append(f"- identity_verification_status: {record.get('identity_verification_status')}")
        lines.append(f"- verification_status: {record.get('verification_status')}")
        lines.append(f"- failure_reason: {record.get('failure_reason')}")
        lines.append("- coefficient_equations:")
        for equation in record.get("coefficient_equations", [])[:8]:
            lines.append(f"    {equation}")
        lines.append("- branch_attempts:")
        for attempt in record.get("branch_attempts", [])[:6]:
            lines.append(f"    {attempt}")
        lines.append("")
    path = results_dir / "failure_analysis.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _write_search_outputs(results_dir: Path, candidates, processed, exact_solutions, alpha, beta, gamma) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)

    (results_dir / "generated_functions.json").write_text(
        json.dumps([sfg._asdict(c) for c in candidates], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    (results_dir / "processed_candidates.json").write_text(
        json.dumps(processed, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    (results_dir / "exact_solutions.json").write_text(
        json.dumps(exact_solutions, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    failed = [r for r in processed if r.get("verification_status") != "EXACT_VERIFIED"]
    (results_dir / "failed_candidates.json").write_text(
        json.dumps(failed, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    verified_candidates = [r for r in processed if r.get("verification_status") == "EXACT_VERIFIED"]
    equivalence_groups: dict[str, list[dict]] = {}
    for solution in exact_solutions:
        equivalence_groups.setdefault(solution["equivalence_key"], []).append(solution)
    distinct_solution_count = len(equivalence_groups)

    seed_candidates = [c for c in candidates if c.source_type == "seed"]
    generated_candidates = [c for c in candidates if c.source_type == "generated"]
    symbolic_success = sum(1 for r in processed if r.get("symbolic_status") == "success")
    constraint_success = sum(1 for r in processed if r.get("constraint_status") == "success")
    solve_success = sum(1 for r in processed if r.get("solve_status") == "success")
    exact_branches = len(exact_solutions)
    exact_candidates = len(verified_candidates)
    category_counts = Counter(r.get("category") for r in processed)
    depth_counts = Counter(r.get("tree_depth") for r in processed)
    node_values = [r.get("node_count", 0) for r in processed]
    complexity_values = [r.get("complexity", 0) for r in processed]
    stage_counts = Counter(_classify_gardner_result(r) for r in processed)

    report_lines = [
        "# SFG + NNSCA Gardner search report",
        "",
        f"- coefficients: alpha={alpha}, beta={beta}, gamma={gamma}",
        f"- generated candidates: {len(candidates)}",
        f"- unique candidates after structural dedup: {len(set(c.expression for c in candidates))}",
        f"- candidates with symbolic analysis success: {symbolic_success}",
        f"- candidates with constraint extraction success: {constraint_success}",
        f"- candidates with solver success: {solve_success}",
        f"- verified exact branches: {exact_branches}",
        f"- verified exact candidates: {exact_candidates}",
        f"- distinct exact solutions after equivalence: {distinct_solution_count}",
        "",
        "## Seed/generated split",
        "",
        f"- seed candidates: {len(seed_candidates)}",
        f"- generated candidates: {len(generated_candidates)}",
        "",
        "## Candidate quality",
        "",
        f"- category distribution: {dict(category_counts)}",
        f"- depth distribution: {dict(depth_counts)}",
        f"- node count range: {min(node_values) if node_values else 0}..{max(node_values) if node_values else 0}",
        f"- complexity range: {min(complexity_values) if complexity_values else 0}..{max(complexity_values) if complexity_values else 0}",
        "",
        "## Result classification",
        "",
        f"{dict(stage_counts)}",
        "",
        "## Verified branches",
        "",
    ]
    for solution in exact_solutions:
        audit = solution.get("audit", {})
        report_lines.append(f"### {solution['function_id']}")
        report_lines.append(f"- source: {solution['source_expression']}")
        report_lines.append(f"- trial: {solution['trial_expression']}")
        report_lines.append(f"- status: {audit.get('status')}")
        report_lines.append(f"- parameter conditions: {audit.get('parameter_conditions', [])}")
        report_lines.append(f"- domain notes: {audit.get('domain_notes', [])}")
        report_lines.append("")
    report_lines += [
        "Only branches whose raw Gardner residual was certified identically zero",
        "by ``_residual_is_zero`` are listed as exact.",
    ]
    (results_dir / "phase1_report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    _write_failure_analysis(results_dir, processed)

    residual_lines = [
        "# Gardner residual verification",
        "",
        f"Raw residual: `u_t + {alpha}*u*u_x + {beta}*u**2*u_x + {gamma}*u_xxx`.",
        "",
        "The cubic term is implemented as `u**2 * diff(u, x)`, not",
        "`u * diff(u, x)**2`.  Third-order space derivatives are computed by",
        "`sp.diff(u, X, 3)`.  No travelling-wave ODE or numerical sampling is",
        "used as an exactness proof.",
        "",
        "| candidate | verification | solver | identity |",
        "|---|---|---|---|",
    ]
    for record in processed:
        residual_lines.append(
            f"| {record['function_id']}: {record['expression']} "
            f"| {record.get('verification_status')} "
            f"| {record.get('solve_status')} "
            f"| {record.get('identity_verification_status')} |"
        )
    (results_dir / "residual_verification.md").write_text(
        "\n".join(residual_lines) + "\n", encoding="utf-8"
    )

    experiment_records = {
        "coefficients": {"alpha": str(alpha), "beta": str(beta), "gamma": str(gamma)},
        "candidates": [sfg._asdict(c) for c in candidates],
        "processed": processed,
        "exact_solutions": exact_solutions,
        "summary": {
            "generated": len(candidates),
            "unique": len(set(c.expression for c in candidates)),
            "symbolic_success": symbolic_success,
            "constraint_success": constraint_success,
            "solve_success": solve_success,
            "exact_branches": exact_branches,
            "exact_candidates": exact_candidates,
            "distinct_solutions": distinct_solution_count,
        },
    }
    (results_dir / "experiment_records.json").write_text(
        json.dumps(experiment_records, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SFG + NNSCA Gardner search")
    parser.add_argument("--max-candidates", type=int, default=None)
    parser.add_argument("--num-candidates", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument(
        "--mode",
        choices=["random", "recursive", "mixed", "generated-only"],
        default=None,
    )
    parser.add_argument("--widths", default="2,1")
    parser.add_argument("--alpha", type=str, default="1")
    parser.add_argument("--beta", type=str, default="1")
    parser.add_argument("--gamma", type=str, default="1")
    parser.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR))
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args(argv)

    alpha = sp.sympify(args.alpha)
    beta = sp.sympify(args.beta)
    gamma = sp.sympify(args.gamma)
    residual_fn = residual_fn_for(alpha=alpha, beta=beta, gamma=gamma)

    config = copy.deepcopy(sfg.DEFAULT_CONFIG)
    num_candidates = args.num_candidates if args.num_candidates is not None else args.max_candidates
    network_widths = sfg._normalise_network_widths([int(x) for x in args.widths.split(",")])
    config["network"]["widths"] = network_widths
    if num_candidates is not None:
        config["generator"]["max_candidates"] = num_candidates
    if args.seed is not None:
        config["generator"]["random_seed"] = args.seed
    if args.mode in ("generated-only",):
        config["generator"]["mode"] = "random"
        config["generator"]["include_seeds"] = False
    elif args.mode in ("mixed", "random"):
        config["generator"]["mode"] = "random"
        config["generator"]["include_seeds"] = True
    elif args.mode == "recursive":
        config["generator"]["mode"] = "recursive"
        config["generator"]["include_seeds"] = True

    start_time = time.time()
    results_dir = Path(args.results_dir).expanduser()
    maple_dir = results_dir / "maple_manual_tasks"
    results_dir.mkdir(parents=True, exist_ok=True)
    maple_dir.mkdir(parents=True, exist_ok=True)

    (results_dir / "run_config.json").write_text(
        json.dumps(
            {
                "argv": argv or [],
                "python_version": sys.version.split()[0],
                "sympy_version": sp.__version__,
                "pde": "gardner",
                "coefficients": {"alpha": str(alpha), "beta": str(beta), "gamma": str(gamma)},
                "config": config,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    candidates = sfg.generate_candidates(config["generator"])
    if args.quick:
        candidates = [c for c in candidates if c.function_id <= "func_0004"]
    unique_candidates = [c for c in candidates if c.duplicate_status == "unique"]

    print("=" * 72)
    print(f"SFG + NNSCA {network_widths} Gardner search")
    print(f"coefficients: alpha={alpha}, beta={beta}, gamma={gamma}")
    print(f"network: {network_widths}")
    print(f"candidates generated: {len(candidates)}")
    print(f"unique candidates: {len(unique_candidates)}")

    log_lines = [
        f"run started at {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"network={network_widths}",
        f"coefficients alpha={alpha} beta={beta} gamma={gamma}",
        f"mode={config['generator']['mode']} seed={config['generator']['random_seed']}",
    ]
    processed = []
    exact_solutions = []
    for idx, candidate in enumerate(unique_candidates, start=1):
        print(f"[{idx}/{len(unique_candidates)}] {candidate.function_id}: {candidate.expression}")
        record = sfg._process_candidate(
            candidate,
            config,
            maple_dir,
            log_lines,
            residual_fn=residual_fn,
            pde_equation=GARDNER_PDE_STR,
            reduce_fn=sfg_reduction.reduce_special_function_expression,
        )
        processed.append(record)
        if record.get("verification_status") == "EXACT_VERIFIED":
            for branch in record.get("exact_solutions", []):
                if network_widths == [2, 1]:
                    audit = audit_exact_solution(
                        candidate.expression, branch["constraints"], alpha=alpha, beta=beta, gamma=gamma
                    )
                else:
                    trial_for_audit = sfg.build_trial(sfg._sympify_f(candidate.expression), network_widths)
                    audit = _audit_trial(
                        trial_for_audit, branch["constraints"], alpha=alpha, beta=beta, gamma=gamma
                    )
                equivalence_key = sfg._solution_equivalence_key(branch["expression"])
                branch["equivalence_key"] = equivalence_key
                branch["audit"] = audit
                exact_solutions.append({
                    "function_id": candidate.function_id,
                    "source_expression": candidate.expression,
                    "source_type": candidate.source_type,
                    "generation_rule": candidate.generation_rule,
                    "trial_expression": branch["expression"],
                    "constraints": branch["constraints"],
                    "residual": branch["residual"],
                    "equivalence_key": equivalence_key,
                    "audit": audit,
                })

    _write_search_outputs(results_dir, candidates, processed, exact_solutions, alpha, beta, gamma)

    log_lines.append(f"elapsed={time.time() - start_time:.2f}s")
    (results_dir / "search_log.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    print("=" * 72)
    print("Summary")
    print(f"  generated: {len(candidates)}")
    print(f"  unique: {len(unique_candidates)}")
    print(f"  exact branches: {len(exact_solutions)}")
    print(f"  results: {results_dir}")
    print("=" * 72)
    for solution in exact_solutions:
        print(f"EXACT {solution['function_id']}: u = {solution['trial_expression']}")
        print(f"  constraints: {solution['constraints']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
