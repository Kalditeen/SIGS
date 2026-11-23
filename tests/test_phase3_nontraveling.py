"""Focused tests for Phase 3-C/D non-travelling structures and classification."""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from nnsca.analysis.traveling_wave import classify_traveling_wave  # noqa: E402
from nnsca.compiler import AnsatzCompiler  # noqa: E402
from sfg.nontraveling import (  # noqa: E402
    multi_phase,
    nontraveling_templates,
    space_time_composite,
    space_time_separated,
    structure_tag,
    traveling_wave_baseline,
)

X, T = sp.symbols("x t", real=True)


def test_all_nontraveling_templates_compile() -> None:
    compiler = AnsatzCompiler()
    for name, ir in nontraveling_templates().items():
        compiled = compiler.compile_ir(ir)
        assert compiled.expression.has(X, T)
        assert compiled.candidate.unknown_parameters


def test_space_time_separated_has_independent_branches() -> None:
    ir = space_time_separated()
    expression = AnsatzCompiler().compile_ir(ir).expression
    assert sp.Symbol("a_px") in expression.free_symbols
    assert sp.Symbol("b_pt") in expression.free_symbols
    assert sp.Symbol("b_px") not in expression.free_symbols
    assert structure_tag(ir) == "SPACE_TIME_SEPARATED"


def test_multi_phase_has_two_phase_coefficients() -> None:
    ir = multi_phase()
    assert len(ir.phases) == 2
    assert structure_tag(ir) == "MULTI_PHASE"


def test_space_time_composite_has_outer_activation() -> None:
    ir = space_time_composite()
    assert structure_tag(ir) == "SPACE_TIME_COMPOSITE"
    assert len(ir.nodes) == 3


def test_traveling_wave_baseline_tag() -> None:
    ir = traveling_wave_baseline()
    assert structure_tag(ir) == "TRAVELING_WAVE_ORIENTED"
    assert len(ir.nodes) == 1


def test_traveling_wave_classifier_recognises_standard_wave() -> None:
    result = classify_traveling_wave(sp.tanh(X - 2 * T), X, T)
    assert result["classification"] == "TRAVELING_WAVE_CONFIRMED"
    assert sp.simplify(result["wave_speed"] - 2) == 0


def test_traveling_wave_classifier_handles_constant() -> None:
    result = classify_traveling_wave(sp.Integer(7), X, T)
    assert result["classification"] == "CONSTANT_OR_DEGENERATE"


def test_traveling_wave_classifier_rejects_spacetime_separated_expression() -> None:
    result = classify_traveling_wave(sp.sin(X) + sp.cos(T), X, T)
    assert result["classification"] == "NON_TRAVELING_WAVE_CANDIDATE"


def test_compiled_traveling_baseline_is_traveling_wave() -> None:
    compiled = AnsatzCompiler().compile_ir(traveling_wave_baseline())
    result = classify_traveling_wave(compiled.expression, X, T)
    assert result["classification"] == "TRAVELING_WAVE_CONFIRMED"
