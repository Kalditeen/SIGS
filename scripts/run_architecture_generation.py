"""Deterministic architecture-generation and compilation experiment.

This script intentionally does not run Stage2 or verify PDE residuals.  It
proves the architecture pipeline: template reproduction, bounded generation,
mutation, canonicalisation, deduplication, compilation, and reproducibility.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from nnsca.compiler import AnsatzCompiler
from sfg.architecture_generator import ArchitectureGenerator, GeneratorConfig
from sfg.architecture_mutation import ArchitectureMutator, MutationConfig
from sfg.candidate_manager import CandidateManager
from sfg.paper_templates import PAPER_TEMPLATES, paper_templates

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "results" / "phase2_architecture_generation"


def _run_experiments(seed: int, num_candidates: int, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    templates = paper_templates()
    manager = CandidateManager()
    template_record_ids: dict[str, str] = {}

    # Experiment A: exact template reproduction.
    for name, builder in PAPER_TEMPLATES.items():
        ir = builder()
        manager.register(
            ir,
            generation_method="paper_template",
            source_type="paper_template",
            category=f"paper_{name}",
            random_seed=seed,
        )
        template_record_ids[name] = manager.records[-1].candidate_id

    # Experiment B: activation mutation.
    mutator = ArchitectureMutator(
        MutationConfig(seed=seed, max_total_nodes=12, max_incoming_edges_per_node=5)
    )
    for name, template_ir in templates.items():
        parent_id = template_record_ids[name]
        for _ in range(3):
            outcome = mutator.mutate(template_ir, "mutate_activation", seed=seed)
            if outcome.valid:
                manager.register(
                    outcome.network,
                    parent_candidate_id=parent_id,
                    generation_method="mutate_activation",
                    mutation_history=outcome.network.metadata.get("mutation_history", []),
                    random_seed=seed,
                )

    # Experiment C: topology mutation.
    for name, template_ir in templates.items():
        for mutation_type in ("add_node", "add_edge", "add_skip_edge", "remove_edge", "rewire_edge"):
            outcome = mutator.mutate(template_ir, mutation_type, seed=seed)
            if outcome.valid:
                manager.register(
                    outcome.network,
                    generation_method=mutation_type,
                    mutation_history=outcome.network.metadata.get("mutation_history", []),
                    random_seed=seed,
                )

    # Experiment D: depth mutation.
    for name, template_ir in templates.items():
        for mutation_type in ("add_layer", "remove_layer", "change_node_layer"):
            outcome = mutator.mutate(template_ir, mutation_type, seed=seed)
            if outcome.valid:
                manager.register(
                    outcome.network,
                    generation_method=mutation_type,
                    mutation_history=outcome.network.metadata.get("mutation_history", []),
                    random_seed=seed,
                )

    # Add a bounded from-scratch generation sample.
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
    for ir in generator.generate(num_candidates, seed=seed):
        manager.register(ir, generation_method="bounded_layered_random", random_seed=seed)

    compile_start = time.perf_counter()
    manager.compile_all()
    compile_wall = time.perf_counter() - compile_start

    # Experiment E: reproducibility.
    run_one_signatures = [
        ir.signature()
        for ir in ArchitectureGenerator(
            GeneratorConfig(
                seed=seed,
                min_depth=1,
                max_depth=2,
                min_nodes_per_layer=1,
                max_nodes_per_layer=2,
                max_total_nodes=5,
            )
        ).generate(num_candidates, seed=seed)
    ]
    run_two_signatures = [
        ir.signature()
        for ir in ArchitectureGenerator(
            GeneratorConfig(
                seed=seed,
                min_depth=1,
                max_depth=2,
                min_nodes_per_layer=1,
                max_nodes_per_layer=2,
                max_total_nodes=5,
            )
        ).generate(num_candidates, seed=seed)
    ]

    stats = manager.stats()
    stats["compile_wall_seconds"] = compile_wall
    stats["reproducible_generation"] = run_one_signatures == run_two_signatures
    stats["reproducible_signature_count"] = len(run_one_signatures)

    manager.save(output_dir / "candidates.json")
    (output_dir / "stats.json").write_text(
        json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (output_dir / "run_config.json").write_text(
        json.dumps({"seed": seed, "num_candidates": num_candidates}, indent=2),
        encoding="utf-8",
    )
    return stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--num-candidates", type=int, default=12)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    stats = _run_experiments(args.seed, args.num_candidates, args.output_dir)
    print(json.dumps(stats, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
