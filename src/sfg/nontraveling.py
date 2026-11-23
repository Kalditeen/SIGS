"""Non-travelling-wave-oriented NetworkIR templates.

These templates intentionally give different hidden nodes independent spatial
and temporal coefficients.  They are structure seeds, not known PDE solutions.
"""

from __future__ import annotations

import sympy as sp

from sfg.network_ir import NetworkIR


def _phase(ir: NetworkIR, node_id: str, x_weight, t_weight, bias) -> None:
    ir.add_phase(
        node_id,
        x_weight=x_weight,
        t_weight=t_weight,
        bias=bias,
    )


def space_time_separated(
    space_activation: str = "sin",
    time_activation: str = "tanh",
) -> NetworkIR:
    """Build F(a1*x + d1) + G(b2*t + d2) with two output nodes."""
    ir = NetworkIR(
        "nontraveling_space_time_separated",
        metadata={"structure_tag": "SPACE_TIME_SEPARATED"},
    )
    _phase(ir, "px", sp.Symbol("a_px"), sp.Integer(0), sp.Symbol("d_px"))
    _phase(ir, "pt", sp.Integer(0), sp.Symbol("b_pt"), sp.Symbol("d_pt"))
    ir.add_compute("sx", space_activation, ["px"])
    ir.add_compute("st", time_activation, ["pt"])
    ir.set_linear_output(["sx", "st"])
    return ir


def space_time_composite(
    space_activation: str = "sin",
    time_activation: str = "cos",
    outer_activation: str = "tanh",
) -> NetworkIR:
    """Build H(F(a1*x + d1) + G(b2*t + d2))."""
    ir = NetworkIR(
        "nontraveling_space_time_composite",
        metadata={"structure_tag": "SPACE_TIME_COMPOSITE"},
    )
    _phase(ir, "px", sp.Symbol("a_px"), sp.Integer(0), sp.Symbol("d_px"))
    _phase(ir, "pt", sp.Integer(0), sp.Symbol("b_pt"), sp.Symbol("d_pt"))
    ir.add_compute("sx", space_activation, ["px"])
    ir.add_compute("st", time_activation, ["pt"])
    ir.add_compute("mix", outer_activation, ["sx", "st"])
    ir.set_linear_output(["mix"])
    return ir


def multi_phase(
    first_activation: str = "sin",
    second_activation: str = "cos",
) -> NetworkIR:
    """Build F(a1*x + b1*t + d1) + G(a2*x + b2*t + d2)."""
    ir = NetworkIR(
        "nontraveling_multi_phase",
        metadata={"structure_tag": "MULTI_PHASE"},
    )
    _phase(ir, "p1", sp.Symbol("a_p1"), sp.Symbol("b_p1"), sp.Symbol("d_p1"))
    _phase(ir, "p2", sp.Symbol("a_p2"), sp.Symbol("b_p2"), sp.Symbol("d_p2"))
    ir.add_compute("f1", first_activation, ["p1"])
    ir.add_compute("f2", second_activation, ["p2"])
    ir.set_linear_output(["f1", "f2"])
    return ir


def traveling_wave_baseline(activation: str = "tanh") -> NetworkIR:
    """Single shared travelling phase, kept as the Phase 3-D baseline."""
    ir = NetworkIR(
        "traveling_wave_baseline",
        metadata={"structure_tag": "TRAVELING_WAVE_ORIENTED"},
    )
    _phase(ir, "p1", sp.Symbol("a_p1"), sp.Symbol("b_p1"), sp.Symbol("d_p1"))
    ir.add_compute("f1", activation, ["p1"])
    ir.set_linear_output(["f1"])
    return ir


def nontraveling_templates() -> dict[str, NetworkIR]:
    return {
        "space_time_separated": space_time_separated(),
        "space_time_composite": space_time_composite(),
        "multi_phase": multi_phase(),
        "traveling_wave_baseline": traveling_wave_baseline(),
    }


def structure_tag(ir: NetworkIR) -> str:
    return ir.metadata.get("structure_tag", "MIXED_HETEROGENEOUS")


__all__ = [
    "multi_phase",
    "nontraveling_templates",
    "space_time_composite",
    "space_time_separated",
    "structure_tag",
    "traveling_wave_baseline",
]
