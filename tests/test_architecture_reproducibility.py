"""Deterministic reproducibility tests for the architecture search pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sfg.architecture_generator import ArchitectureGenerator, GeneratorConfig  # noqa: E402
from sfg.architecture_mutation import ArchitectureMutator, MutationConfig  # noqa: E402
from sfg.candidate_manager import CandidateManager  # noqa: E402
from sfg.paper_templates import paper_templates  # noqa: E402


def _generator(seed: int) -> ArchitectureGenerator:
    return ArchitectureGenerator(
        GeneratorConfig(seed=seed, min_depth=1, max_depth=2, max_nodes_per_layer=2, max_total_nodes=5)
    )


def test_generated_signatures_match_across_runs() -> None:
    first = _generator(99).generate(8, seed=99)
    second = _generator(99).generate(8, seed=99)
    assert [ir.signature() for ir in first] == [ir.signature() for ir in second]


def test_different_seeds_can_change_results() -> None:
    first = _generator(101).generate(6, seed=101)
    second = _generator(202).generate(6, seed=202)
    # The sampler has more than one reachable architecture for these bounds.
    assert first[0].signature() != second[0].signature()


def test_mutation_reproducibility() -> None:
    parent = paper_templates()["2231"]
    first = ArchitectureMutator(MutationConfig(seed=55)).mutate(parent, "add_node", seed=55)
    second = ArchitectureMutator(MutationConfig(seed=55)).mutate(parent, "add_node", seed=55)
    assert first.network.signature() == second.network.signature()
    assert first.changed_nodes == second.changed_nodes


def test_compile_status_is_deterministic() -> None:
    first = CandidateManager()
    second = CandidateManager()
    for ir in _generator(77).generate(5, seed=77):
        first.register(ir)
        second.register(ir)
    first.compile_all()
    second.compile_all()
    assert [r.compile_status for r in first.records] == [r.compile_status for r in second.records]
    assert [r.expression for r in first.records] == [r.expression for r in second.records]
