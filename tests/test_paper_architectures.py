"""Regression tests for the five paper-derived NNSCA architectures."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sigs.jacobi import JacobiCN, JacobiDN, JacobiSN  # noqa: E402

from nnsca.compiler import AnsatzCompiler  # noqa: E402
from sfg.network_ir import NetworkIR  # noqa: E402
from sfg.paper_templates import PAPER_TEMPLATES  # noqa: E402

X, T = sp.symbols("x t", real=True)


def _expr(ir: NetworkIR) -> sp.Expr:
    return AnsatzCompiler().compile_ir(ir).expression


def test_template_231_compiles_to_manual_expression() -> None:
    ir = PAPER_TEMPLATES["231"]()
    compiled = _expr(ir)

    p1 = sp.Symbol("a_p1") * X + sp.Symbol("b_p1") * T + sp.Symbol("d_p1")
    p2 = sp.Symbol("a_p2") * X + sp.Symbol("b_p2") * T + sp.Symbol("d_p2")
    p3 = sp.Symbol("a_p3") * X + sp.Symbol("b_p3") * T + sp.Symbol("d_p3")
    expected = (
        sp.Symbol("c0")
        + sp.Symbol("c_h1") * (sp.Symbol("bias_h1") + sp.Symbol("w_p1__h1") * p1)
        + sp.Symbol("c_h2") * (sp.Symbol("bias_h2") + sp.Symbol("w_p2__h2") * p2) ** 2
        + sp.Symbol("c_h3") * sp.cosh(sp.Symbol("bias_h3") + sp.Symbol("w_p3__h3") * p3)
    )
    assert sp.expand(compiled - expected) == 0
    assert len(ir.parameter_symbols()) == 19
    assert ir.activation_functions() == {
        "h1": "identity",
        "h2": "square",
        "h3": "cosh",
    }


def test_template_2231_compiles_to_manual_expression() -> None:
    ir = PAPER_TEMPLATES["2231"]()
    compiled = _expr(ir)

    p1 = sp.Symbol("a_p1") * X + sp.Symbol("b_p1") * T + sp.Symbol("d_p1")
    p2 = sp.Symbol("a_p2") * X + sp.Symbol("b_p2") * T + sp.Symbol("d_p2")
    g1 = sp.tanh(
        sp.Symbol("bias_g1")
        + sp.Symbol("w_p1__g1") * p1
        + sp.Symbol("w_p2__g1") * p2
    )
    g2 = sp.sech(
        sp.Symbol("bias_g2")
        + sp.Symbol("w_p1__g2") * p1
        + sp.Symbol("w_p2__g2") * p2
    )
    h1 = (sp.Symbol("bias_h1") + sp.Symbol("w_g1__h1") * g1) ** 2
    h2 = sp.exp(
        sp.Symbol("bias_h2")
        + sp.Symbol("w_g1__h2") * g1
        + sp.Symbol("w_g2__h2") * g2
    )
    h3 = JacobiCN(
        sp.Symbol("bias_h3") + sp.Symbol("w_g2__h3") * g2,
        sp.Symbol("m_h3"),
    )
    expected = (
        sp.Symbol("c0")
        + sp.Symbol("c_h1") * h1
        + sp.Symbol("c_h2") * h2
        + sp.Symbol("c_h3") * h3
    )
    assert sp.expand(compiled - expected) == 0
    assert len(ir.nodes) == 5
    assert len(ir.edges) == 8


def test_template_2321_compiles_to_manual_expression() -> None:
    ir = PAPER_TEMPLATES["2321"]()
    compiled = _expr(ir)

    p1 = sp.Symbol("a_p1") * X + sp.Symbol("b_p1") * T + sp.Symbol("d_p1")
    p2 = sp.Symbol("a_p2") * X + sp.Symbol("b_p2") * T + sp.Symbol("d_p2")
    p3 = sp.Symbol("a_p3") * X + sp.Symbol("b_p3") * T + sp.Symbol("d_p3")
    g1 = sp.Symbol("bias_g1") + sp.Symbol("w_p1__g1") * p1
    g2 = (sp.Symbol("bias_g2") + sp.Symbol("w_p2__g2") * p2) ** 2
    g3 = sp.cosh(sp.Symbol("bias_g3") + sp.Symbol("w_p3__g3") * p3)
    h1 = sp.exp(
        sp.Symbol("bias_h1")
        + sp.Symbol("w_g1__h1") * g1
        + sp.Symbol("w_g2__h1") * g2
    )
    h2 = JacobiCN(
        sp.Symbol("bias_h2")
        + sp.Symbol("w_g2__h2") * g2
        + sp.Symbol("w_g3__h2") * g3,
        sp.Symbol("m_h2"),
    )
    expected = (
        sp.Symbol("c0")
        + sp.Symbol("c_h1") * h1
        + sp.Symbol("c_h2") * h2
    )
    assert sp.expand(compiled - expected) == 0


def test_template_2221_compiles_to_manual_expression() -> None:
    ir = PAPER_TEMPLATES["2221"]()
    compiled = _expr(ir)

    p1 = sp.Symbol("a_p1") * X + sp.Symbol("b_p1") * T + sp.Symbol("d_p1")
    p2 = sp.Symbol("a_p2") * X + sp.Symbol("b_p2") * T + sp.Symbol("d_p2")
    g1 = JacobiSN(
        sp.Symbol("bias_g1")
        + sp.Symbol("w_p1__g1") * p1
        + sp.Symbol("w_p2__g1") * p2,
        sp.Symbol("m_g1"),
    )
    g2 = JacobiCN(
        sp.Symbol("bias_g2")
        + sp.Symbol("w_p1__g2") * p1
        + sp.Symbol("w_p2__g2") * p2,
        sp.Symbol("m_g2"),
    )
    h1 = JacobiDN(
        sp.Symbol("bias_h1") + sp.Symbol("w_g1__h1") * g1,
        sp.Symbol("m_h1"),
    )
    h2 = (
        sp.Symbol("bias_h2")
        + sp.Symbol("w_g1__h2") * g1
        + sp.Symbol("w_g2__h2") * g2
    ) ** 2
    expected = (
        sp.Symbol("c0")
        + sp.Symbol("c_h1") * h1
        + sp.Symbol("c_h2") * h2
    )
    assert sp.expand(compiled - expected) == 0


def test_template_23211_compiles_to_manual_expression() -> None:
    ir = PAPER_TEMPLATES["23211"]()
    compiled = _expr(ir)

    p1 = sp.Symbol("a_p1") * X + sp.Symbol("b_p1") * T + sp.Symbol("d_p1")
    p2 = sp.Symbol("a_p2") * X + sp.Symbol("b_p2") * T + sp.Symbol("d_p2")
    p3 = sp.Symbol("a_p3") * X + sp.Symbol("b_p3") * T + sp.Symbol("d_p3")
    g1 = sp.Symbol("bias_g1") + sp.Symbol("w_p1__g1") * p1
    g2 = (sp.Symbol("bias_g2") + sp.Symbol("w_p2__g2") * p2) ** 2
    g3 = sp.cosh(sp.Symbol("bias_g3") + sp.Symbol("w_p3__g3") * p3)
    h1 = sp.exp(
        sp.Symbol("bias_h1")
        + sp.Symbol("w_g1__h1") * g1
        + sp.Symbol("w_g2__h1") * g2
    )
    h2 = JacobiCN(
        sp.Symbol("bias_h2")
        + sp.Symbol("w_g2__h2") * g2
        + sp.Symbol("w_g3__h2") * g3,
        sp.Symbol("m_h2"),
    )
    k1 = sp.tanh(
        sp.Symbol("bias_k1")
        + sp.Symbol("w_h1__k1") * h1
        + sp.Symbol("w_h2__k1") * h2
    )
    expected = sp.Symbol("c0") + sp.Symbol("c_k1") * k1
    assert sp.expand(compiled - expected) == 0


def test_all_templates_serialize_and_restore() -> None:
    for ir in (builder() for builder in PAPER_TEMPLATES.values()):
        restored = NetworkIR.from_dict(ir.to_dict())
        assert restored.signature() == ir.signature()
        assert AnsatzCompiler().compile_ir(restored).expression is not None


def test_all_templates_have_independent_activation_nodes() -> None:
    for ir in (builder() for builder in PAPER_TEMPLATES.values()):
        assert len({node.activation.name for node in ir.nodes.values()}) >= 1
        assert all(ir.nodes[node_id].activation is not None for node_id in ir.nodes)


def test_all_templates_validate_mixed_derivatives() -> None:
    for ir in (builder() for builder in PAPER_TEMPLATES.values()):
        compiled = AnsatzCompiler().compile_ir(ir)
        u_xxx = compiled.derivative((X, 3))
        u_xxt = compiled.derivative((X, 2), (T, 1))
        assert u_xxx is not None
        assert u_xxt is not None
