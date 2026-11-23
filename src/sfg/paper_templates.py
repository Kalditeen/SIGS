"""Programmatic reconstruction of five paper-derived NNSCA architectures.

These builders return :class:`~sfg.network_ir.NetworkIR` objects.  They are
intended as regression templates for the compiler and structural analysis.
The connection patterns below are the explicit computation graphs used by the
task's five frameworks; they are kept sparse where the paper architectures are
not plain fully-connected layers.
"""

from __future__ import annotations

from sfg.activation_registry import activation_by_name
from sfg.network_ir import NetworkIR


def _ir(name: str) -> NetworkIR:
    return NetworkIR(ir_id=name, metadata={"source": "paper_architecture_template"})


def template_231() -> NetworkIR:
    ir = _ir("paper_framework_231")
    for idx, phase in enumerate(("p1", "p2", "p3")):
        ir.add_phase(phase)
    ir.add_compute("h1", "identity", ["p1"])
    ir.add_compute("h2", "square", ["p2"])
    ir.add_compute("h3", "cosh", ["p3"])
    ir.set_linear_output(["h1", "h2", "h3"])
    return ir


def template_2231() -> NetworkIR:
    ir = _ir("paper_framework_2231")
    for phase in ("p1", "p2"):
        ir.add_phase(phase)
    ir.add_compute("g1", "tanh", ["p1", "p2"])
    ir.add_compute("g2", "sech", ["p1", "p2"])
    ir.add_compute("h1", "square", ["g1"])
    ir.add_compute("h2", "exp", ["g1", "g2"])
    ir.add_compute("h3", "JacobiCN", ["g2"])
    ir.set_linear_output(["h1", "h2", "h3"])
    return ir


def template_2321() -> NetworkIR:
    ir = _ir("paper_framework_2321")
    for phase in ("p1", "p2", "p3"):
        ir.add_phase(phase)
    ir.add_compute("g1", "identity", ["p1"])
    ir.add_compute("g2", "square", ["p2"])
    ir.add_compute("g3", "cosh", ["p3"])
    ir.add_compute("h1", "exp", ["g1", "g2"])
    ir.add_compute("h2", "JacobiCN", ["g2", "g3"])
    ir.set_linear_output(["h1", "h2"])
    return ir


def template_2221() -> NetworkIR:
    ir = _ir("paper_framework_2221")
    for phase in ("p1", "p2"):
        ir.add_phase(phase)
    ir.add_compute("g1", "JacobiSN", ["p1", "p2"])
    ir.add_compute("g2", "JacobiCN", ["p1", "p2"])
    ir.add_compute("h1", "JacobiDN", ["g1"])
    ir.add_compute("h2", "square", ["g1", "g2"])
    ir.set_linear_output(["h1", "h2"])
    return ir


def template_23211() -> NetworkIR:
    ir = _ir("paper_framework_23211")
    for phase in ("p1", "p2", "p3"):
        ir.add_phase(phase)
    ir.add_compute("g1", "identity", ["p1"])
    ir.add_compute("g2", "square", ["p2"])
    ir.add_compute("g3", "cosh", ["p3"])
    ir.add_compute("h1", "exp", ["g1", "g2"])
    ir.add_compute("h2", "JacobiCN", ["g2", "g3"])
    ir.add_compute("k1", "tanh", ["h1", "h2"])
    ir.set_linear_output(["k1"])
    return ir


PAPER_TEMPLATES = {
    "231": template_231,
    "2231": template_2231,
    "2321": template_2321,
    "2221": template_2221,
    "23211": template_23211,
}


def paper_templates() -> dict[str, NetworkIR]:
    return {name: builder() for name, builder in PAPER_TEMPLATES.items()}
