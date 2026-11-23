"""Tests for NetworkIR structural mutation operators."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sfg.architecture_mutation import ArchitectureMutator, MutationConfig  # noqa: E402
from sfg.architecture_utils import hidden_depth  # noqa: E402
from sfg.paper_templates import paper_templates  # noqa: E402


def _mutator() -> ArchitectureMutator:
    return ArchitectureMutator(MutationConfig(seed=5, max_total_nodes=12, max_incoming_edges_per_node=5))


def test_mutation_never_mutates_parent() -> None:
    parent = paper_templates()["2231"]
    before = parent.to_dict()
    outcome = _mutator().mutate(parent, "mutate_activation", seed=5)
    assert outcome.valid
    assert parent.to_dict() == before
    assert outcome.network.ir_id != parent.ir_id


def test_activation_mutation_changes_exactly_one_node() -> None:
    parent = paper_templates()["2231"]
    outcome = _mutator().mutate(parent, "mutate_activation", seed=9)
    assert outcome.valid
    assert len(outcome.changed_nodes) == 1
    node_id = outcome.changed_nodes[0]
    assert outcome.network.nodes[node_id].activation.name != parent.nodes[node_id].activation.name


@pytest.mark.parametrize(
    "mutation_type",
    ["add_node", "remove_node", "add_edge", "add_skip_edge", "remove_edge", "rewire_edge"],
)
def test_common_mutations_are_valid(mutation_type: str) -> None:
    parent = paper_templates()["2231"]
    outcome = _mutator().mutate(parent, mutation_type, seed=10)
    assert outcome.valid, outcome
    outcome.network.validate()


def test_add_layer_increases_depth() -> None:
    parent = paper_templates()["2231"]
    old_depth = hidden_depth(parent)
    outcome = _mutator().mutate(parent, "add_layer", seed=12)
    assert outcome.valid
    assert hidden_depth(outcome.network) == old_depth + 1
    assert len(outcome.changed_nodes) >= 1


def test_remove_layer_decreases_depth() -> None:
    parent = paper_templates()["2231"]
    old_depth = hidden_depth(parent)
    outcome = _mutator().mutate(parent, "remove_layer", seed=13)
    assert outcome.valid
    assert hidden_depth(outcome.network) == old_depth - 1


def test_remove_only_layer_is_invalid() -> None:
    parent = paper_templates()["231"]
    outcome = _mutator().mutate(parent, "remove_layer", seed=14)
    assert not outcome.valid


def test_mutation_reproducible_with_seed() -> None:
    parent = paper_templates()["2231"]
    first = _mutator().mutate(parent, "add_edge", seed=42)
    second = _mutator().mutate(parent, "add_edge", seed=42)
    assert first.network.signature() == second.network.signature()
    assert first.changed_edges == second.changed_edges
