"""Tests for the bounded NetworkIR architecture generator."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sfg.architecture_generator import ArchitectureGenerator, GeneratorConfig  # noqa: E402
from sfg.network_ir import NetworkIR  # noqa: E402
from sfg.paper_templates import paper_templates  # noqa: E402


def _config(**kwargs) -> GeneratorConfig:
    values = dict(seed=7, min_depth=1, max_depth=2, max_nodes_per_layer=2, max_total_nodes=5)
    values.update(kwargs)
    return GeneratorConfig(**values)


def test_generate_is_deterministic() -> None:
    first = ArchitectureGenerator(_config()).generate(5, seed=7)
    second = ArchitectureGenerator(_config()).generate(5, seed=7)
    assert [ir.signature() for ir in first] == [ir.signature() for ir in second]
    assert [ir.ir_id for ir in first] == [ir.ir_id for ir in second]


def test_generated_networks_are_valid_and_bounded() -> None:
    config = _config(min_depth=1, max_depth=2, max_nodes_per_layer=2, max_total_nodes=5)
    results = ArchitectureGenerator(config).generate(6, seed=3)
    assert len(results) == 6
    for ir in results:
        ir.validate()
        assert 1 <= len(ir.phases) <= config.max_phases
        assert 1 <= len(ir.nodes) <= config.max_total_nodes
        assert ir.output_terms
        assert len({node.activation.name for node in ir.nodes.values()}) >= 1


def test_unknown_activation_is_rejected() -> None:
    with pytest.raises(ValueError):
        GeneratorConfig(activation_pool=("not_an_activation",))


def test_generate_from_template_preserves_derivation() -> None:
    base = paper_templates()["2231"]
    generated = ArchitectureGenerator(_config(seed=11, max_total_nodes=10)).generate_from_template(base, count=3, seed=11)
    assert len(generated) == 3
    assert all(isinstance(ir, NetworkIR) for ir in generated)
    assert all(ir.metadata.get("derived_from") == base.ir_id for ir in generated)
    base_signature = base.signature()
    assert all(ir.signature() != base_signature for ir in generated)


def test_output_structure_respected() -> None:
    config = _config(output_structure="all_hidden_linear", min_depth=1, max_depth=1)
    ir = ArchitectureGenerator(config).generate(1, seed=2)[0]
    assert {term.source for term in ir.output_terms} == set(ir.nodes)
