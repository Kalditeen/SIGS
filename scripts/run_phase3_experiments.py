#!/usr/bin/env python3
"""Run the Phase 3 Gardner experiments E1-E4/E6.

The script never hardcodes a known solution.  It constructs IR candidates,
runs the existing Stage2 adapter through ``AutomaticSolver``, and saves each
experiment under a fresh timestamped directory.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import sympy as sp

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
PDES = REPO_ROOT / "scripts" / "pdes"
for path in (SRC, PDES):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import sfg_bbm_21 as sfg  # noqa: E402

from nnsca.analysis.traveling_wave import classify_traveling_wave  # noqa: E402
from nnsca.compiler import AnsatzCompiler  # noqa: E402
from nnsca.search.automatic_solver import AutomaticSolver, AutomaticSolverConfig  # noqa: E402
from nnsca.search.representative_selector import (  # noqa: E402
    CATEGORY_NAMES,
    select_representative_candidates,
    structure_profile,
)
from sfg.architecture_generator import ArchitectureGenerator, GeneratorConfig  # noqa: E402
from sfg.candidate_manager import CandidateManager  # noqa: E402
from sfg.network_ir import Edge, NetworkIR  # noqa: E402
from sfg.nontraveling import nontraveling_templates, structure_tag  # noqa: E402

DEFAULT_CANDIDATES = (
    REPO_ROOT / "results" / "phase2_architecture_generation" / "candidates.json"
)


def _now_id() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _solver_config(args: argparse.Namespace) -> AutomaticSolverConfig:
    return AutomaticSolverConfig(
        extract_timeout=args.extract_timeout,
        solve_timeout=args.solve_timeout,
        residual_timeout=args.residual_timeout,
        verify_timeout=args.verify_timeout,
        max_expression_nodes=args.max_expression_nodes,
    )


def _benchmark_ir() -> NetworkIR:
    """Single-node JacobiCN regression candidate. No solution is hardcoded."""
    ir = NetworkIR("phase3_benchmark_jacobi_cn")
    ir.add_phase("p1", x_weight="a", t_weight="b", bias="d")
    ir.add_compute("h1", "JacobiCN", ["p1"], bias="0")
    edge = ir.edges[("p1", "h1")]
    ir.edges[("p1", "h1")] = Edge(edge.edge_id, edge.source, edge.target, sp.Integer(1))
    ir.set_linear_output(["h1"])
    ir.validate()
    return ir


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _jacobi_benchmark_ir(activation: str) -> NetworkIR:
    """Single-node Jacobi benchmark candidate. No solution is hardcoded."""
    ir = NetworkIR(f"phase3_benchmark_{activation}")
    ir.add_phase("p1", x_weight="a", t_weight="b", bias="d")
    ir.add_compute("h1", activation, ["p1"], bias="0")
    edge = ir.edges[("p1", "h1")]
    ir.edges[("p1", "h1")] = Edge(edge.edge_id, edge.source, edge.target, sp.Integer(1))
    ir.set_linear_output(["h1"])
    ir.validate()
    return ir


def _serialize_wave(wave: dict) -> dict:
    wave = dict(wave)
    if wave.get("wave_speed") is not None:
        wave["wave_speed"] = sp.sstr(wave["wave_speed"])
    return wave


def cmd_benchmark(args: argparse.Namespace) -> int:
    manager = CandidateManager()
    records = []
    for activation in ("JacobiCN", "JacobiSN", "JacobiDN"):
        records.append(
            manager.register(
                _jacobi_benchmark_ir(activation),
                generation_method="phase3_benchmark",
                source_type="seed",
                category=f"jacobi_{activation}",
                random_seed=args.seed,
            )
        )
    config = _solver_config(args)
    config.candidate_ids = tuple(record.candidate_id for record in records)
    run_data = AutomaticSolver().run(manager, config)
    record = records[0]

    output_dir = args.output_dir or (REPO_ROOT / "results" / "phase3_benchmark")
    run_dir = AutomaticSolver.save_run(run_data, config, output_dir, run_id=_now_id())
    benchmark = {
        "candidate_id": record.candidate_id,
        "candidate_ids": [r.candidate_id for r in records],
        "status": run_data["results"][0]["status"],
        "stage2": run_data["results"][0].get("stage2_record"),
        "exact_solutions": run_data["exact_solutions"],
        "statistics": run_data["statistics"],
    }
    _write_json(run_dir / "benchmark.json", benchmark)

    print(json.dumps(run_data["statistics"], indent=2, ensure_ascii=False))
    print(f"run_dir={run_dir}")
    return 0


def cmd_complex(args: argparse.Namespace) -> int:
    manager = CandidateManager.load(args.candidates)
    selected = select_representative_candidates(
        manager,
        per_category=1,
        allow_overlap=False,
    )
    category_selection: dict[str, dict] = {}
    missing_categories: list[str] = []
    candidate_ids: list[str] = []
    for label in CATEGORY_NAMES:
        records = selected[label]
        if not records:
            missing_categories.append(label)
            continue
        record = records[0]
        profile = structure_profile(record)
        category_selection[label] = {
            "candidate_id": record.candidate_id,
            "node_count": profile.node_count,
            "depth": profile.depth,
            "activation_names": profile.activation_names,
            "categories": profile.categories,
        }
        candidate_ids.append(record.candidate_id)

    config = _solver_config(args)
    config.candidate_ids = tuple(sorted(set(candidate_ids)))
    run_data = AutomaticSolver().run(manager, config)
    run_data["statistics"]["category_selection"] = category_selection
    run_data["statistics"]["missing_categories"] = missing_categories

    output_dir = args.output_dir or (REPO_ROOT / "results" / "phase3_complex_network_audit")
    run_dir = AutomaticSolver.save_run(run_data, config, output_dir, run_id=_now_id())

    report_lines = [
        "# Phase 3-B Complex Network Audit",
        "",
        "This audit selects real Phase 2 candidates for six structural",
        "categories and runs each through the original Gardner Stage2 path.",
        "A candidate may represent more than one category, so the table records",
        "its full structural profile.",
        "",
        "## Selection",
        "",
        "| category | candidate | nodes | depth | activations |",
        "|---|---|---|---|---|",
    ]
    for label in CATEGORY_NAMES:
        if label in missing_categories:
            report_lines.append(f"| {label} | missing | | | |")
            continue
        info = category_selection[label]
        report_lines.append(
            f"| {label} | {info['candidate_id']} | {info['node_count']} "
            f"| {info['depth']} | {', '.join(info['activation_names'])} |"
        )
    if missing_categories:
        report_lines.append("")
        report_lines.append(
            f"Missing categories: {', '.join(missing_categories)}. These were not "
            "fabricated."
        )

    report_lines.extend([
        "",
        "## Results",
        "",
        "| candidate | status | degeneracy | failure reason |",
        "|---|---|---|---|",
    ])
    for result in run_data["results"]:
        report_lines.append(
            f"| {result['candidate_id']} | {result['status']} "
            f"| {result.get('degeneracy_status', 'UNKNOWN')} "
            f"| {result.get('failure_reason') or ''} |"
        )
    report_lines.extend([
        "",
        "## Failure-stage distribution",
        "",
    ])
    for status, count in sorted(run_data["statistics"]["status_counts"].items()):
        report_lines.append(f"- {status}: {count}")
    report_lines.extend([
        "",
        "Only branches certified by raw Gardner residual identity are reported as",
        "exact.  A failed solve is recorded as a failure stage, never as a proof",
        "that no exact solution exists.",
        "",
    ])
    (REPO_ROOT / "docs" / "phase3").mkdir(parents=True, exist_ok=True)
    (REPO_ROOT / "docs" / "phase3" / "PHASE3_COMPLEX_NETWORK_AUDIT.md").write_text(
        "\n".join(report_lines) + "\n", encoding="utf-8"
    )

    print(json.dumps(run_data["statistics"], indent=2, ensure_ascii=False))
    print(f"run_dir={run_dir}")
    return 0


def cmd_multiseed(args: argparse.Namespace) -> int:
    seeds = [int(seed) for seed in args.seeds.split(",") if seed.strip()]
    experiments = []
    signature_sets: dict[int, set[str]] = {}
    output_dir = args.output_dir or (REPO_ROOT / "results" / "phase3_multiseed")
    run_dir = output_dir / f"run_{_now_id()}"
    run_dir.mkdir(parents=True, exist_ok=True)

    for seed in seeds:
        generator = ArchitectureGenerator(
            GeneratorConfig(
                seed=seed,
                min_depth=1,
                max_depth=2,
                min_nodes_per_layer=1,
                max_nodes_per_layer=2,
                max_total_nodes=5,
                max_total_edges=20,
            )
        )
        manager = CandidateManager()
        for ir in generator.generate(args.num_candidates, seed=seed):
            manager.register(
                ir,
                generation_method="phase3_multiseed",
                random_seed=seed,
            )
        compile_start = time.perf_counter()
        manager.compile_all()
        compile_wall = time.perf_counter() - compile_start
        unique = manager.unique_records()
        signature_sets[seed] = {record.structure_signature for record in unique}

        solve_ids = [
            record.candidate_id
            for record in sorted(
                unique,
                key=lambda record: (
                    len(record.network_ir.nodes),
                    len(record.network_ir.edges),
                    record.candidate_id,
                ),
            )[: args.solve_per_seed]
        ]
        config = _solver_config(args)
        config.candidate_ids = tuple(solve_ids)
        run_data = AutomaticSolver().run(manager, config)

        stats = manager.stats()
        stats.update({
            "compile_wall_seconds": compile_wall,
            "solve_result": {
                "candidate_ids": solve_ids,
                "statistics": run_data["statistics"],
                "exact_solutions": run_data["exact_solutions"],
            },
        })
        experiments.append({"seed": seed, "statistics": stats})

    overlap = {}
    for left in seeds:
        for right in seeds:
            if left >= right:
                continue
            a = signature_sets[left]
            b = signature_sets[right]
            union = len(a | b)
            overlap[f"{left}_{right}"] = {
                "left_count": len(a),
                "right_count": len(b),
                "intersection": len(a & b),
                "jaccard": round(len(a & b) / union, 4) if union else None,
            }

    payload = {
        "seeds": seeds,
        "num_candidates": args.num_candidates,
        "solve_per_seed": args.solve_per_seed,
        "experiments": experiments,
        "signature_overlap": overlap,
    }
    _write_json(run_dir / "multi_seed_experiment.json", payload)

    report_lines = [
        "# Phase 3 Multi-seed Experiment",
        "",
        f"Seeds: {', '.join(str(seed) for seed in seeds)}",
        f"Generated per seed: {args.num_candidates}",
        f"Solved per seed: up to {args.solve_per_seed} simplest unique candidates",
        "",
        "| seed | generated | unique | compiled | solved | exact branches |",
        "|---|---|---|---|---|---|",
    ]
    for experiment in experiments:
        stats = experiment["statistics"]
        solve = stats["solve_result"]["statistics"]
        report_lines.append(
            f"| {experiment['seed']} | {stats['generated_candidates']} "
            f"| {stats['unique_candidates']} | {stats['compiler_success_count']} "
            f"| {solve['candidate_total']} | {solve['exact_branches']} |"
        )
    report_lines.extend([
        "",
        "## Signature overlap",
        "",
        "| seed pair | left | right | intersection | jaccard |",
        "|---|---|---|---|---|",
    ])
    for key, value in sorted(overlap.items()):
        report_lines.append(
            f"| {key} | {value['left_count']} | {value['right_count']} "
            f"| {value['intersection']} | {value['jaccard']} |"
        )
    (run_dir / "multi_seed_report.md").write_text(
        "\n".join(report_lines) + "\n", encoding="utf-8"
    )

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"run_dir={run_dir}")
    return 0


def cmd_nontraveling(args: argparse.Namespace) -> int:
    manager = CandidateManager()
    templates = nontraveling_templates()
    for name, ir in templates.items():
        manager.register(
            ir,
            generation_method=f"nontraveling_template:{name}",
            source_type="nontraveling_template",
            category=structure_tag(ir),
            random_seed=args.seed,
        )
    manager.compile_all()

    config = _solver_config(args)
    config.candidate_ids = tuple(record.candidate_id for record in manager.unique_records())
    run_data = AutomaticSolver().run(manager, config)

    structure_info = {}
    for name, ir in templates.items():
        compiled = AnsatzCompiler().compile_ir(ir)
        structure_info[name] = {
            "structure_tag": structure_tag(ir),
            "node_count": len(ir.nodes),
            "phase_count": len(ir.phases),
            "expression": sp.sstr(compiled.expression),
            "parameter_count": len(compiled.candidate.unknown_parameters),
            "traveling_wave": classify_traveling_wave(
                compiled.expression, sfg.X, sfg.T
            ),
        }
    run_data["statistics"]["structure_info"] = structure_info
    for info in structure_info.values():
        info["traveling_wave"] = _serialize_wave(info["traveling_wave"])

    output_dir = args.output_dir or (REPO_ROOT / "results" / "phase3_nontraveling")
    run_dir = AutomaticSolver.save_run(run_data, config, output_dir, run_id=_now_id())
    _write_json(run_dir / "structure_info.json", structure_info)

    report_lines = [
        "# Phase 3-C/D Non-travelling Analysis",
        "",
        "The structures below are templates, not known solutions.  Their labels",
        "describe the network shape only; the mathematical travelling-wave test",
        "is run separately and never assumes non-travelling behaviour.",
        "",
        "## Template profiles",
        "",
        "| template | tag | nodes | phases | parameters | wave classification |",
        "|---|---|---|---|---|---|",
    ]
    for name, info in structure_info.items():
        report_lines.append(
            f"| {name} | {info['structure_tag']} | {info['node_count']} "
            f"| {info['phase_count']} | {info['parameter_count']} "
            f"| {info['traveling_wave']['classification']} |"
        )
    report_lines.extend([
        "",
        "## Stage2 results",
        "",
        "| candidate | status | degeneracy | failure reason |",
        "|---|---|---|---|",
    ])
    for result in run_data["results"]:
        report_lines.append(
            f"| {result['candidate_id']} | {result['status']} "
            f"| {result.get('degeneracy_status', 'UNKNOWN')} "
            f"| {result.get('failure_reason') or ''} |"
        )
    if run_data["exact_solutions"]:
        report_lines.extend([
            "",
            "## Verified exact branches and travelling-wave classification",
            "",
        ])
        for solution in run_data["exact_solutions"]:
            wave = solution["traveling_wave"]
            report_lines.append(
                f"- {solution['candidate_id']}: "
                f"{solution['expression']} -> {wave['classification']}"
            )
    (REPO_ROOT / "docs" / "phase3").mkdir(parents=True, exist_ok=True)
    (REPO_ROOT / "docs" / "phase3" / "PHASE3_NONTRAVELING_ANALYSIS.md").write_text(
        "\n".join(report_lines) + "\n", encoding="utf-8"
    )

    print(json.dumps(run_data["statistics"], indent=2, ensure_ascii=False))
    print(f"run_dir={run_dir}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 3 Gardner experiments")
    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--seed", type=int, default=2026)
    common.add_argument("--output-dir", type=Path, default=None)
    common.add_argument("--extract-timeout", type=float, default=6.0)
    common.add_argument("--solve-timeout", type=float, default=8.0)
    common.add_argument("--residual-timeout", type=float, default=6.0)
    common.add_argument("--verify-timeout", type=float, default=8.0)
    common.add_argument("--max-expression-nodes", type=int, default=4000)

    parser_benchmark = subparsers.add_parser("benchmark", parents=[common])
    parser_benchmark.set_defaults(func=cmd_benchmark)

    parser_complex = subparsers.add_parser("complex", parents=[common])
    parser_complex.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser_complex.set_defaults(func=cmd_complex)

    parser_multiseed = subparsers.add_parser("multiseed", parents=[common])
    parser_multiseed.add_argument("--num-candidates", type=int, default=12)
    parser_multiseed.add_argument("--solve-per-seed", type=int, default=3)
    parser_multiseed.add_argument("--seeds", default="101,202,303")
    parser_multiseed.set_defaults(func=cmd_multiseed)

    parser_nontraveling = subparsers.add_parser("nontraveling", parents=[common])
    parser_nontraveling.set_defaults(func=cmd_nontraveling)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
