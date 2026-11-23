"""Cross-equation compatibility tests for the revised Phase 1 compiler."""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from nnsca.adapter import Stage2Input  # noqa: E402
from sigs.jacobi import reduce_jacobi_powers  # noqa: E402
from nnsca.compiler import AnsatzCompiler  # noqa: E402
from pdes.ch import ch_residual  # noqa: E402
from pdes.gardner import gardner_residual  # noqa: E402
from sfg.network_ir import NetworkIR  # noqa: E402
from sfg.paper_templates import PAPER_TEMPLATES  # noqa: E402

X, T = sp.symbols("x t", real=True)


def test_paper_templates_compile_for_gardner_and_ch() -> None:
    compiler = AnsatzCompiler()
    for builder in PAPER_TEMPLATES.values():
        ir = builder()
        compiled = compiler.compile_ir(ir)
        assert gardner_residual(compiled.expression) is not None
        assert ch_residual(compiled.expression) is not None


def test_stage2_input_carries_structure_trace() -> None:
    ir = PAPER_TEMPLATES["231"]()
    compiled = AnsatzCompiler().compile_ir(ir)
    stage2_input = Stage2Input(
        pde=gardner_residual,
        expression=compiled.expression,
        unknown_parameters=ir.parameter_symbols(),
        parameter_roles=ir.parameter_roles(),
        candidate_id=ir.ir_id,
        network_structure=ir.to_dict(),
    )
    assert stage2_input.candidate_id == "paper_framework_231"
    assert stage2_input.network_structure["ir_id"] == "paper_framework_231"
    assert any("phase" in role for role in stage2_input.parameter_roles)


def test_gardner_jacobi_cn_known_branch_is_external_only() -> None:
    ir = NetworkIR("gardner_jacobi_cn_probe")
    ir.add_phase("p1", x_weight="k", t_weight="-k*(4*c1**2 - 12*k**2 - 3)/12", bias="0")
    ir.add_compute("h1", "JacobiCN", ["p1"], bias="0")
    ir.set_linear_output(["h1"], output_bias="-1/2")
    compiled = AnsatzCompiler().compile_ir(ir)

    substitution = {
        sp.Symbol("m_h1"): sp.sympify("c1**2/(6*k**2)"),
        sp.Symbol("w_p1__h1"): sp.Integer(1),
        sp.Symbol("c_h1"): sp.Symbol("c1"),
    }
    u = sp.expand(compiled.expression.subs(substitution))
    residual = sp.expand(gardner_residual(u))
    # External benchmark only; no solver module receives this parameter relation.
    assert sp.expand(reduce_jacobi_powers(residual)) == 0
