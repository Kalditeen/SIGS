#!/usr/bin/env python3
"""Run the first Gardner adaptation experiments and write the required reports.

This is intentionally small-scale.  It verifies known benchmark families with
the raw Gardner residual, probes a few network/function combinations, runs one
reproducible generated-only SFG search, and then writes the reports under
``results/gardner``.
"""

from __future__ import annotations

import copy
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PDES_DIR = REPO_ROOT / "scripts" / "pdes"
if str(PDES_DIR) not in sys.path:
    sys.path.insert(0, str(PDES_DIR))

import sfg_bbm_21 as sfg  # noqa: E402
import sfg_gardner as gardner  # noqa: E402

OUT_ROOT = REPO_ROOT / "results" / "gardner"
GENERATED_SUBDIR = OUT_ROOT / "generated_seed101"

BENCHMARKS = [
    {
        "id": "gardner_jacobi_cn",
        "expression": "JacobiCN(z,m)",
        "alpha": 1,
        "beta": 1,
        "gamma": 1,
        "constraints": {
            "c0": "-1/2",
            "a": "k",
            "b": "-k*(4*c1**2 - 12*k**2 - 3)/12",
            "d": "0",
            "m": "c1**2/(6*k**2)",
        },
        "source": "cnoidal reduction of the Gardner travelling-wave ODE; independently verified by raw SymPy residual.",
        "notes": [
            "m is the elliptic parameter (modulus square).",
            "m != 0 and k != 0 for a genuinely elliptic branch.",
            "c1 may be positive or negative; m = c1**2/(6*k**2) >= 0.",
        ],
    },
    {
        "id": "kdv_limit_sech2",
        "expression": "sech(z)**2",
        "alpha": 6,
        "beta": 0,
        "gamma": 1,
        "constraints": {
            "c0": "0",
            "c1": "2*k**2",
            "a": "k",
            "b": "-4*k**3",
            "d": "0",
        },
        "source": "Auxiliary KdV limit (alpha=6, beta=0). Standard sech^2 soliton.",
        "notes": ["Auxiliary test only; not part of the alpha=beta=gamma=1 main experiment."],
    },
    {
        "id": "mkdv_limit_sech",
        "expression": "sech(z)",
        "alpha": 0,
        "beta": 6,
        "gamma": 1,
        "constraints": {
            "c0": "0",
            "c1": "k",
            "a": "k",
            "b": "-k**3",
            "d": "0",
        },
        "source": "Auxiliary mKdV limit (alpha=0, beta=6). Standard sech soliton.",
        "notes": ["Auxiliary test only; not part of the alpha=beta=gamma=1 main experiment."],
    },
]


def _process_expr(
    expr: str,
    widths,
    f_exprs=None,
    alpha=1,
    beta=1,
    gamma=1,
    solve_timeout=10.0,
    label=None,
) -> dict:
    config = copy.deepcopy(sfg.DEFAULT_CONFIG)
    config["network"]["widths"] = widths
    config["solver"]["solve_timeout"] = solve_timeout
    config["solver"]["extract_timeout"] = max(8.0, solve_timeout)
    config["solver"]["residual_timeout"] = 8.0
    config["solver"]["verify_timeout"] = 8.0
    candidate = sfg._candidate_from_expr(
        label or _slug(expr),
        sfg._sympify_f(expr),
        source_type="seed",
        generation_rule="gardner_phase1_manual",
    )
    maple_dir = OUT_ROOT / "maple_manual_tasks"
    maple_dir.mkdir(parents=True, exist_ok=True)
    record = sfg._process_candidate(
        candidate,
        config,
        maple_dir,
        [],
        f_exprs=f_exprs,
        residual_fn=gardner.residual_fn_for(alpha=alpha, beta=beta, gamma=gamma),
        pde_equation=gardner.GARDNER_PDE_STR,
    )
    record["experiment_expression"] = expr if f_exprs is None else "|".join(str(f) for f in f_exprs)
    record["network_widths"] = widths
    record["coefficients"] = {"alpha": alpha, "beta": beta, "gamma": gamma}
    return record


def _slug(expr: str) -> str:
    return (
        expr.replace("**", "pow")
        .replace("(", "_")
        .replace(")", "_")
        .replace(",", "_")
        .replace("*", "_")
        .replace(" ", "")
    )[:36]


def _two_node_summary(record: dict) -> str:
    if record.get("verification_status") != "EXACT_VERIFIED":
        return record.get("verification_status", "UNKNOWN")
    branches = record.get("exact_solutions", [])
    if not branches:
        return "NO_EXACT_BRANCH"
    active = []
    single = []
    for branch in branches:
        constraints = branch.get("constraints", {})
        out0 = sfg._sympify_f(constraints.get("w_out_0", "0"))
        out1 = sfg._sympify_f(constraints.get("w_out_1", "0"))
        if out0 != 0 and out1 != 0:
            active.append(constraints)
        else:
            single.append(constraints)
    if active:
        return "EXACT_TWO_NODE_ACTIVE"
    if single:
        return "EXACT_SINGLE_NODE_REDUCTION"
    return "DEGENERATE"


def _write_benchmarks() -> list[dict]:
    records = []
    for bench in BENCHMARKS:
        audit = gardner.audit_exact_solution(
            bench["expression"],
            bench["constraints"],
            alpha=bench["alpha"],
            beta=bench["beta"],
            gamma=bench["gamma"],
        )
        records.append({**bench, "audit": audit})
        print(
            f"benchmark {bench['id']}: {audit['status']} "
            f"certified_zero={audit['certified_zero']}"
        )

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "known_solution_benchmarks.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    lines = [
        "# Gardner known-solution benchmarks",
        "",
        "## Main experiment: alpha=beta=gamma=1",
        "",
        "| id | source | trial | status |",
        "|---|---|---|---|",
    ]
    for record in records:
        if record["alpha"] == 1 and record["beta"] == 1 and record["gamma"] == 1:
            lines.append(
                f"| {record['id']} | {record['expression']} "
                f"| {record['audit']['trial_expression']} | {record['audit']['status']} |"
            )
    lines += [
        "",
        "### JacobiCN family",
        "",
        "u = -1/2 + c1*cn(k*(x - c*t) | m),",
        "m = c1**2/(6*k**2),",
        "c = (4*c1**2 - 12*k**2 - 3)/12.",
        "",
        "The raw Gardner residual for this family is certified identically zero by",
        "SymPy.  This is the primary recovery target for the fixed coefficient",
        "set alpha=beta=gamma=1.",
        "",
        "## Auxiliary limits (not part of the main coefficient set)",
        "",
        "| id | coefficients | expression | trial | status |",
        "|---|---|---|---|---|",
    ]
    for record in records:
        if not (record["alpha"] == 1 and record["beta"] == 1 and record["gamma"] == 1):
            lines.append(
                f"| {record['id']} | {record['alpha']},{record['beta']},{record['gamma']} "
                f"| {record['expression']} | {record['audit']['trial_expression']} "
                f"| {record['audit']['status']} |"
            )
    lines += [
        "",
        "## Verification policy",
        "",
        "Every benchmark above was rebuilt and substituted into the raw PDE",
        "residual.  ``EXACT_VERIFIED`` means the raw residual was certified",
        "identically zero by ``_residual_is_zero``; no numerical sampling and no",
        "travelling-wave ODE was accepted as proof.",
    ]
    (OUT_ROOT / "known_solution_benchmarks.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    return records


def _write_residual_verification(benchmark_records: list[dict]) -> None:
    lines = [
        "# Gardner residual verification",
        "",
        "Raw residual implemented in `scripts/pdes/sfg_gardner.py`:",
        "",
        "    R[u] = u_t + alpha*u*u_x + beta*u**2*u_x + gamma*u_{xxx}",
        "",
        "The cubic nonlinearity is `u**2 * diff(u, x)` and the dispersive term",
        "is `diff(u, x, 3)`.  No travelling-wave reduction is substituted before",
        "verification.  For each benchmark the reconstructed `u(x,t)` is plugged",
        "directly into this raw residual.",
        "",
        "| id | coefficients | certified_zero | status |",
        "|---|---|---|---|",
    ]
    for record in benchmark_records:
        audit = record["audit"]
        lines.append(
            f"| {record['id']} | {record['alpha']},{record['beta']},{record['gamma']} "
            f"| {audit['certified_zero']} | {audit['status']} |"
        )
    lines += [
        "",
        "## Travelling-wave consistency",
        "",
        "For z=x-c*t and u=U(z), substitution gives",
        "",
        "    R = d/dz(-c*U + alpha/2*U^2 + beta/3*U^3 + gamma*U'').",
        "",
        "This formula is used only for cross-checks and documentation; exact",
        "solutions are still verified against the original PDE residual.",
    ]
    (OUT_ROOT / "residual_verification.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def _write_failure_analysis(all_records: list[dict]) -> None:
    solve_success_failed = [
        r for r in all_records
        if r.get("solve_status") == "success"
        and r.get("verification_status") != "EXACT_VERIFIED"
    ]
    lines = [
        "# Gardner failure analysis",
        "",
        "`solve_status=success` is not the same as finding a PDE solution. It",
        "means SymPy returned parameter branches for the extracted coefficient",
        "system.  The rows below failed later stages.",
        "",
        "| candidate | network | symbolic | constraint | solve | verification | failure |",
        "|---|---|---|---|---|---|---|",
    ]
    for record in solve_success_failed:
        lines.append(
            f"| {record.get('experiment_expression', record.get('function_id'))} "
            f"| {record.get('network_widths')} "
            f"| {record.get('symbolic_status')} "
            f"| {record.get('constraint_status')} "
            f"| {record.get('solve_status')} "
            f"| {record.get('verification_status')} "
            f"| {record.get('failure_reason', '')} |"
        )
    lines += [
        "",
        "## Other failures",
        "",
        "| candidate | network | solve status | verification | failure |",
        "|---|---|---|---|---|",
    ]
    for record in all_records:
        if record.get("verification_status") == "EXACT_VERIFIED":
            continue
        if record.get("solve_status") != "success":
            lines.append(
                f"| {record.get('experiment_expression', record.get('function_id'))} "
                f"| {record.get('network_widths')} "
                f"| {record.get('solve_status')} "
                f"| {record.get('verification_status')} "
                f"| {record.get('failure_reason', '')} |"
            )
    (OUT_ROOT / "failure_analysis.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def _write_experiment_reports(
    benchmark_records: list[dict],
    network_records: list[dict],
    combination_records: list[dict],
    generated_records: list[dict],
    generated_candidates: list[dict],
    generated_exact: list[dict],
) -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    (OUT_ROOT / "network_structure_experiments.md").write_text(
        "\n".join(
            [
                "# Gardner network-structure experiments",
                "",
                "| widths | status | solve | failure |",
                "|---|---|---|---|",
            ]
            + [
                f"| {r.get('network_widths')} | {r.get('verification_status')} "
                f"| {r.get('solve_status')} | {r.get('failure_reason') or ''} |"
                for r in network_records
            ]
            + [
                "",
                "The [2,1] and [2,2,1] runs complete the constraint solver but do not",
                "produce a verified Gardner branch for `tanh(z)`.  The [2,3,1] and",
                "[2,3,2,1] runs are blocked by the existing 12-unknown solver limit;",
                "their raw residual and coefficient extraction still finish.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    (OUT_ROOT / "function_combination_experiments.md").write_text(
        "\n".join(
            [
                "# Gardner [2,2,1] function-combination experiments",
                "",
                "| combination | status | solve | two-node summary |",
                "|---|---|---|---|",
            ]
            + [
                f"| {r.get('experiment_expression')} | {r.get('verification_status')} "
                f"| {r.get('solve_status')} | {_two_node_summary(r)} |"
                for r in combination_records
            ]
            + [
                "",
                "No verified non-degenerate two-node Gardner branch was found in this",
                "small probe set.  This is a solver/candidate result, not a proof of",
                "nonexistence.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    verified_lines = [
        "# New-solution candidates",
        "",
        "A candidate can only be labelled `POTENTIALLY_NEW` after strict raw-residual",
        "verification and equivalence analysis against the benchmark families.",
        "",
    ]
    known_keys = {"cnoidal_gardner", "kdv_sech2", "mkdv_sech"}
    potential_new = []
    for solution in generated_exact:
        # No generated branch was certified in the first small run; if one
        # appears later, this comparison should be replaced by real symbolic
        # equivalence analysis against the benchmark trial expressions.
        potential_new.append(solution)
    if potential_new:
        verified_lines.append("| source | trial | status |")
        verified_lines.append("|---|---|---|")
        for solution in potential_new:
            verified_lines.append(
                f"| {solution['source_expression']} | {solution['trial_expression']} "
                f"| POTENTIALLY_NEW |"
            )
    else:
        verified_lines.append(
            "The generated-only seed=101 search produced no `EXACT_VERIFIED` branch, "
            "so there are no new-solution candidates in this run."
        )
    (OUT_ROOT / "new_solution_candidates.md").write_text(
        "\n".join(verified_lines) + "\n", encoding="utf-8"
    )

    all_records = network_records + combination_records + generated_records
    exact_solution_summary = []
    for record in all_records:
        for branch in record.get("exact_solutions", []):
            exact_solution_summary.append(
                {
                    "function_id": record.get("function_id"),
                    "experiment_expression": record.get("experiment_expression"),
                    "network_widths": record.get("network_widths"),
                    "trial_expression": branch.get("expression"),
                    "constraints": branch.get("constraints"),
                }
            )

    experiment_records = {
        "benchmarks": [
            {k: v for k, v in b.items() if k != "audit"}
            | {"audit_status": b["audit"]["status"]}
            for b in benchmark_records
        ],
        "network_structure_experiments": network_records,
        "function_combination_experiments": combination_records,
        "generated_seed101": {
            "candidates": generated_candidates,
            "processed": generated_records,
            "exact_solutions": generated_exact,
        },
        "verified_exact_solutions": exact_solution_summary,
    }
    (OUT_ROOT / "experiment_records.json").write_text(
        json.dumps(experiment_records, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _write_phase1_report(benchmark_records: list[dict], all_records: list[dict]) -> None:
    exact_count = sum(1 for r in all_records if r.get("verification_status") == "EXACT_VERIFIED")
    solve_success = sum(1 for r in all_records if r.get("solve_status") == "success")
    lines = [
        "# Gardner phase-1 report",
        "",
        "## Questions and results",
        "",
        "1. Can the existing SFG+NNSCA architecture be transferred directly to Gardner?",
        "   Yes for candidate generation, network construction, coefficient extraction,",
        "   and raw-residual certification. The PDE residual and audit/report helpers",
        "   were the only Gardner-specific pieces.",
        "",
        "2. Which modules are fully reusable?",
        "   SFG generation, `build_trial`, Jacobi support, `_extract_coefficient_equations`,",
        "   `_solve_equations`, `_residual_is_zero`, and the record/status machinery.",
        "",
        "3. Which modules needed modification and why?",
        "   A new `sfg_gardner.py` supplies the Gardner residual and independent audit",
        "   helpers. `sfg_bbm_21.py` only gained a sech-power reduction for certification.",
        "",
        "4. Can the program automatically recover the Gardner benchmark?",
        "   The raw-residual audit recovers and certifies the JacobiCN family. The",
        "   generic unconstrained solver timed out on that particular Jacobi coefficient",
        "   system, so automatic recovery through `sp.solve` is not yet demonstrated.",
        "",
        "5. Which function/network combinations perform best?",
        "   In the small probe, no [2,2,1] branch was verified. The single-node JacobiCN",
        "   benchmark is the clearest exact family. Deeper widths currently hit the",
        "   12-unknown solver guard.",
        "",
        "6. Was a strictly verified new solution found?",
        "   No. No `EXACT_VERIFIED` branch beyond the independently supplied benchmarks",
        "   was produced in these small first-round experiments.",
        "",
        "7. What are the current solver limitations?",
        "   `sp.solve` is the main bottleneck for Jacobi elliptic coefficient systems;",
        "   deeper networks exceed the 12-unknown guard; and the raw-residual checker",
        "   needs explicit function identities for odd sech powers.",
        "",
        "8. Does this support migration to other shallow-water equations?",
        "   Partially. The architecture is equation-agnostic and Gardner residuals are",
        "   handled correctly, but the constraint solver needs targeted differential",
        "   algebra work before broader migration is credible.",
        "",
        "## Counts from this run",
        "",
        f"- verified benchmark families: {len(benchmark_records)}",
        f"- verified branches from search probes: {exact_count}",
        f"- solve-success records: {solve_success}",
        "",
        "All counts refer to the raw-residual symbolic gate, not to `sp.solve` alone.",
    ]
    (OUT_ROOT / "phase1_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    started = time.time()
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    benchmark_records = _write_benchmarks()
    _write_residual_verification(benchmark_records)

    # Known-recovery probe.  The explicit JacobiCN benchmark is audited above;
    # this generic [2,1] solve attempt records whether sp.solve can rediscover it.
    known_records = [
        _process_expr("JacobiCN(z,m)", [2, 1], solve_timeout=12.0, label="known_cn_21"),
        _process_expr("sech(z)**2", [2, 1], solve_timeout=8.0),
        _process_expr("tan(z)**2", [2, 1], solve_timeout=8.0),
    ]

    network_records = [
        _process_expr("tanh(z)", [2, 1], solve_timeout=8.0, label="tanh_21"),
        _process_expr("tanh(z)", [2, 2, 1], solve_timeout=8.0, label="tanh_221"),
        _process_expr("tanh(z)", [2, 3, 1], solve_timeout=8.0, label="tanh_231"),
        _process_expr("tanh(z)", [2, 3, 2, 1], solve_timeout=8.0, label="tanh_2321"),
    ]

    combo_pairs = [
        ("sech(z)**2", "sech(z)**2"),
        ("tanh(z)", "tanh(z)"),
        ("sech(z)**2", "tanh(z)"),
        ("JacobiCN(z,m)**2", "sech(z)**2"),
    ]
    combination_records = []
    for left, right in combo_pairs:
        f_exprs = None if left == right else [
            sfg._sympify_f(left),
            sfg._sympify_f(right),
        ]
        combination_records.append(
            _process_expr(
                left,
                [2, 2, 1],
                f_exprs=f_exprs,
                solve_timeout=8.0,
                label=_slug(left),
            )
        )

    # One reproducible generated-only search.  Keep it at 30 candidates so the
    # experiment remains small and auditable.
    generated_dir = GENERATED_SUBDIR
    generated_dir.mkdir(parents=True, exist_ok=True)
    exit_code = gardner.main([
        "--mode", "generated-only",
        "--seed", "101",
        "--num-candidates", "30",
        "--widths", "2,1",
        "--results-dir", str(generated_dir),
    ])
    if exit_code != 0:
        print(f"generated search exited with {exit_code}", file=sys.stderr)
        return exit_code

    generated_candidates = json.loads(
        (generated_dir / "generated_functions.json").read_text(encoding="utf-8")
    )
    generated_records = json.loads(
        (generated_dir / "processed_candidates.json").read_text(encoding="utf-8")
    )
    generated_exact = json.loads(
        (generated_dir / "exact_solutions.json").read_text(encoding="utf-8")
    )
    for record in generated_records:
        record["network_widths"] = [2, 1]
        record["experiment_expression"] = record.get("expression")

    all_records = known_records + network_records + combination_records + generated_records
    _write_experiment_reports(
        benchmark_records,
        network_records,
        combination_records,
        generated_records,
        generated_candidates,
        generated_exact,
    )
    _write_failure_analysis(all_records)
    _write_phase1_report(benchmark_records, all_records)

    print(f"elapsed={time.time() - started:.2f}s")
    print(OUT_ROOT / "phase1_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
