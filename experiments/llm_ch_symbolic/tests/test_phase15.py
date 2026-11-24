"""Phase 1.5 deterministic tests that do not call the LLM API."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import activation_registry, benchmark_generator, symbolic_rule_registry  # noqa: E402
from src.network_ir_adapter import (  # noqa: E402
    compile_expression,
    reference_structure,
    shared_subexpressions,
    topology_summary,
)
from src.residual_analyzer import camassa_holm_residual  # noqa: E402
from src.strategy_validator import validate_analysis, validate_strategy  # noqa: E402
from src.symbolic_executor import execute_strategy  # noqa: E402


def _level1_ir():
    return benchmark_generator.generate_benchmarks(1)[0]


def _level2_ir():
    return benchmark_generator.generate_benchmarks(2)[0]


def _level3_ir():
    return benchmark_generator.generate_benchmarks(3)[1]


def test_ir_compiles_to_expression() -> None:
    ir = _level1_ir()
    u = compile_expression(ir, activation_registry)
    assert u.has(sp.exp)


def test_heterogeneous_activation_inventory() -> None:
    ir = _level2_ir()
    inventory = topology_summary(ir)["activation_inventory"]
    assert "exp" in inventory and "sinh" in inventory


def test_multilayer_topology_has_expected_depth() -> None:
    ir = _level3_ir()
    assert topology_summary(ir)["max_depth"] >= 3


def test_shared_subexpression_detection() -> None:
    ir = benchmark_generator.generate_benchmarks(4)[0]
    assert "z_shared" in shared_subexpressions(ir)


def test_analysis_rejects_unknown_node_id() -> None:
    ir = _level1_ir()
    result = validate_analysis(
        ir,
        {
            "network_type": "single_layer_homogeneous",
            "activation_inventory": [{"node_id": "does_not_exist", "activation": "exp"}],
            "composite_relations": [],
            "shared_subexpressions": [],
            "symbolic_difficulty": [],
            "unsupported_components": [],
        },
    )
    assert result["ok"] is False
    assert any("unknown node_id" in error for error in result["errors"])


def test_strategy_rejects_unknown_rule_id() -> None:
    ir = _level1_ir()
    analysis = validate_analysis(
        ir,
        {
            "network_type": "single_layer_homogeneous",
            "activation_inventory": [
                {"node_id": "q1", "activation": "exp"},
                {"node_id": "q2", "activation": "exp"},
            ],
            "composite_relations": [],
            "shared_subexpressions": [],
            "symbolic_difficulty": [],
            "unsupported_components": [],
        },
    )
    result = validate_strategy(
        ir,
        analysis["normalized"],
        {
            "generators": [],
            "selected_derivative_rules": ["der_not_real"],
            "selected_identity_rules": [],
            "intermediate_variables": [],
            "rewrite_strategy": [],
            "collection_strategy": [],
            "expected_structure": [],
            "unsupported_rules": [],
            "confidence_notes": [],
        },
    )
    assert result["ok"] is False
    assert any("unknown derivative rule" in error for error in result["errors"])


def test_strategy_rejects_inapplicable_rule() -> None:
    ir = _level1_ir()
    analysis = validate_analysis(
        ir,
        {
            "network_type": "single_layer_homogeneous",
            "activation_inventory": [
                {"node_id": "q1", "activation": "exp"},
                {"node_id": "q2", "activation": "exp"},
            ],
            "composite_relations": [],
            "shared_subexpressions": [],
            "symbolic_difficulty": [],
            "unsupported_components": [],
        },
    )
    result = validate_strategy(
        ir,
        analysis["normalized"],
        {
            "generators": [],
            "selected_derivative_rules": ["der_sinh"],
            "selected_identity_rules": [],
            "intermediate_variables": [],
            "rewrite_strategy": [],
            "collection_strategy": [],
            "expected_structure": [],
            "unsupported_rules": [],
            "confidence_notes": [],
        },
    )
    assert result["ok"] is False
    assert any("inapplicable derivative" in error for error in result["errors"])


def test_identity_rewrite_preserves_equivalence() -> None:
    ir = benchmark_generator.generate_benchmarks(2)[2]
    u = compile_expression(ir, activation_registry)
    residual = camassa_holm_residual(u)
    strategy = {
        "selected_derivative_rules": symbolic_rule_registry.derivative_rule_ids(),
        "selected_identity_rules": ["id_cosh_sinh"],
    }
    result = execute_strategy(ir, strategy)
    assert result["compile_status"] == "success"
    assert all(item["equivalent"] for item in result["identity_rewrites"])


def test_raw_residual_is_nonzero_for_arbitrary_network() -> None:
    ir = _level2_ir()
    u = compile_expression(ir, activation_registry)
    assert sp.expand(camassa_holm_residual(u)) != 0


def test_reference_structure_is_deterministic() -> None:
    ir = _level3_ir()
    first = reference_structure(ir)
    second = reference_structure(ir)
    assert first == second
