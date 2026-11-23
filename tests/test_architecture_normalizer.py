"""Tests for structural canonicalisation and deduplication."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sfg.architecture_mutation import ArchitectureMutator, MutationConfig  # noqa: E402
from sfg.architecture_normalizer import ArchitectureNormalizer, canonical_network_ir  # noqa: E402
from sfg.network_ir import NetworkIR  # noqa: E402
from sfg.paper_templates import paper_templates  # noqa: E402


def test_canonicalization_is_idempotent() -> None:
    ir = paper_templates()["2231"]
    once = canonical_network_ir(ir)
    twice = canonical_network_ir(once)
    assert once.signature() == twice.signature()


def test_renamed_ir_is_structurally_equivalent() -> None:
    ir = paper_templates()["2231"]
    renamed = NetworkIR.from_dict(ir.to_dict())
    renamed.ir_id = "renamed"
    assert ArchitectureNormalizer().structurally_equivalent(ir, renamed)


def test_changed_activation_is_not_equivalent() -> None:
    ir = paper_templates()["2231"]
    mutator = ArchitectureMutator(MutationConfig(seed=1))
    changed = mutator.mutate(ir, "mutate_activation", seed=1).network
    assert not ArchitectureNormalizer().structurally_equivalent(ir, changed)


def test_normalizer_does_not_mutate_input() -> None:
    ir = paper_templates()["2231"]
    before = ir.to_dict()
    ArchitectureNormalizer().normalize(ir)
    assert ir.to_dict() == before


def test_unreachable_nodes_are_reported_not_deleted() -> None:
    ir = paper_templates()["231"]
    # Add a compute node that is intentionally not connected to the output.
    ir.add_compute("orphan", "square", ["p1"])
    ir.set_linear_output(["h1", "h2", "h3"])
    normalized = ArchitectureNormalizer().normalize(ir)
    assert "orphan" in normalized.unreachable_nodes
    assert "orphan" in normalized.network.metadata["canonical_ids"]


def test_duplicate_topology_has_same_signature() -> None:
    first = paper_templates()["231"]
    second = paper_templates()["231"]
    assert ArchitectureNormalizer().normalize(first).signature == ArchitectureNormalizer().normalize(second).signature
