"""Tests for effective-network structural-degeneration analysis."""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from nnsca.analysis import analyze_effective_network  # noqa: E402
from nnsca.compiler import AnsatzCompiler  # noqa: E402
from sfg.paper_templates import PAPER_TEMPLATES  # noqa: E402


def test_zero_output_weight_is_classified_trivial() -> None:
    ir = PAPER_TEMPLATES["231"]()
    constraints = {str(term.weight): 0 for term in ir.output_terms}
    result = analyze_effective_network(ir, constraints)
    assert result.classification == "EXACT_TRIVIAL"
    assert result.active_outputs == []
    assert ir.ir_id == "paper_framework_231"


def test_zero_edge_weight_removes_node_from_reachable_set() -> None:
    ir = PAPER_TEMPLATES["2321"]()
    edge = ir.edges[("g1", "h1")]
    constraints = {edge.weight: 0}
    result = analyze_effective_network(ir, constraints)
    assert edge.edge_id in result.inactive_edges
    assert "g1" in result.unreachable_nodes
    assert "g1" not in result.active_nodes


def test_single_active_output_is_single_node() -> None:
    ir = PAPER_TEMPLATES["2231"]()
    constraints = {
        ir.output_terms[0].weight: 1,
        ir.output_terms[1].weight: 0,
        ir.output_terms[2].weight: 0,
    }
    result = analyze_effective_network(ir, constraints)
    assert result.classification == "EXACT_SINGLE_NODE"


def test_analysis_preserves_original_ir() -> None:
    ir = PAPER_TEMPLATES["2221"]()
    original_signature = ir.signature()
    constraints = {ir.output_terms[0].weight: 0}
    analyze_effective_network(ir, constraints)
    assert ir.signature() == original_signature


def test_reduced_expression_is_available_with_compiler() -> None:
    ir = PAPER_TEMPLATES["231"]()
    compiler = AnsatzCompiler()
    constraints = {
        ir.output_terms[0].weight: 0,
        ir.output_terms[1].weight: 0,
        ir.output_terms[2].weight: 1,
    }
    result = analyze_effective_network(ir, constraints, compiler=compiler)
    assert result.reduced_expression is not None
    reduced = sp.sympify(result.reduced_expression)
    assert sp.Symbol("c_h3") not in reduced.free_symbols
    assert reduced.has(sp.cosh)
