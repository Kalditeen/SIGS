#!/usr/bin/env python3
"""Lazy symbolic DAG for Gardner phase 4.

Unlike ``sfg_graph.py``, this module keeps every hidden node and its cached
first/second/third derivatives as persistent objects.  It does not expand the
full output after construction.  Expansion is explicit and only used when a
caller needs the fully expanded SymPy expression for comparison, constraint
extraction, or residual certification.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import sympy as sp

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
PDES_DIR = REPO_ROOT / "scripts" / "pdes"
for path in (SRC_DIR, PDES_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import sfg_bbm_21 as sfg  # noqa: E402

X, T, Z = sfg.X, sfg.T, sfg.Z


@dataclass
class SymbolicNode:
    node_id: str
    layer: int
    index: int
    activation_kind: str
    z: sp.Expr
    h: sp.Expr
    h_x: sp.Expr
    h_t: sp.Expr
    h_xx: sp.Expr
    h_xxx: sp.Expr
    children: list[str] = field(default_factory=list)


class NetworkDAG:
    """A retained network graph with per-node derivative caching.

    The output and residual are kept unexpanded by default.  ``expanded_*``
    methods deliberately materialise SymPy expressions only where needed.
    """

    def __init__(self, widths, activation=None):
        self.widths = list(widths)
        self._validate_widths()
        self.activation = self._coerce_activation(activation)
        self.activation_kind = self._activation_kind(self.activation)
        self.nodes: dict[str, SymbolicNode] = {}
        self.layers: list[list[SymbolicNode]] = []
        self.output_weights: dict[int, sp.Symbol] = {}
        self.u_unexpanded: sp.Expr | None = None
        self._build()

    def _validate_widths(self) -> None:
        if (
            len(self.widths) < 2
            or self.widths[0] != 2
            or self.widths[-1] != 1
        ):
            raise ValueError("widths must start with 2 and end with 1")

    @staticmethod
    def _coerce_activation(activation):
        if activation is None:
            return sp.tanh(Z)
        if isinstance(activation, str):
            return sfg._sympify_f(activation)
        return activation

    @staticmethod
    def _activation_kind(activation) -> str:
        text = str(activation)
        for name in ("JacobiCN", "JacobiSN", "JacobiDN", "sech", "tanh", "exp", "sin", "cos"):
            if name in text:
                return name
        return "custom"

    def _activation_derivatives(self, z_expr: sp.Expr):
        f = self.activation
        fp_expr = sp.diff(f, Z)
        fpp_expr = sp.diff(f, Z, 2)
        fppp_expr = sp.diff(f, Z, 3)
        return (
            f.subs(Z, z_expr),
            fp_expr.subs(Z, z_expr),
            fpp_expr.subs(Z, z_expr),
            fppp_expr.subs(Z, z_expr),
        )

    def _input_nodes(self):
        return [
            SymbolicNode(
                "input_x", 0, 0, "input", X, X, sp.Integer(1), sp.Integer(0),
                sp.Integer(0), sp.Integer(0), [],
            ),
            SymbolicNode(
                "input_t", 0, 1, "input", T, T, sp.Integer(0), sp.Integer(1),
                sp.Integer(0), sp.Integer(0), [],
            ),
        ]

    def _make_node(self, layer: int, index: int, previous: list[SymbolicNode]) -> SymbolicNode:
        node_id = f"h{layer}_{index}"
        z_expr = sp.Symbol(f"b{layer}_{index}")
        z_x = sp.Integer(0)
        z_t = sp.Integer(0)
        z_xx = sp.Integer(0)
        z_xxx = sp.Integer(0)
        for input_idx, node in enumerate(previous):
            w = sp.Symbol(f"w{layer}_{index}_{input_idx}")
            z_expr += w * node.h
            z_x += w * node.h_x
            z_t += w * node.h_t
            z_xx += w * node.h_xx
            z_xxx += w * node.h_xxx
            node.children.append(node_id)

        fz, fp, fpp, fppp = self._activation_derivatives(z_expr)
        return SymbolicNode(
            node_id=node_id,
            layer=layer,
            index=index,
            activation_kind=self.activation_kind,
            z=z_expr,
            h=fz,
            h_x=fp * z_x,
            h_t=fp * z_t,
            h_xx=fpp * z_x**2 + fp * z_xx,
            h_xxx=fppp * z_x**3 + 3 * fpp * z_x * z_xx + fp * z_xxx,
            children=[],
        )

    def _build(self) -> None:
        hidden = self.widths[1:-1]
        if self.widths == [2, 1]:
            node = SymbolicNode(
                node_id="h1_0",
                layer=1,
                index=0,
                activation_kind=self.activation_kind,
                z=sp.Symbol("a") * X + sp.Symbol("b") * T + sp.Symbol("d"),
                h=None,
                h_x=None,
                h_t=None,
                h_xx=None,
                h_xxx=None,
                children=[],
            )
            fz, fp, fpp, fppp = self._activation_derivatives(node.z)
            node.h = fz
            node.h_x = fp * sp.Symbol("a")
            node.h_t = fp * sp.Symbol("b")
            node.h_xx = fpp * sp.Symbol("a") ** 2
            node.h_xxx = fppp * sp.Symbol("a") ** 3
            self.nodes[node.node_id] = node
            self.layers = [[node]]
            self.u_unexpanded = sp.Symbol("c0") + sp.Symbol("c1") * node.h
            return

        previous = self._input_nodes()
        self.layers = []
        for layer_idx, width in enumerate(hidden, start=1):
            current = [self._make_node(layer_idx, index, previous) for index in range(width)]
            self.layers.append(current)
            for node in current:
                self.nodes[node.node_id] = node
            previous = current

        u = sp.Symbol("b_out")
        for node_idx, node in enumerate(self.layers[-1]):
            weight = sp.Symbol(f"w_out_{node_idx}")
            self.output_weights[node_idx] = weight
            u += weight * node.h
        self.u_unexpanded = u

    def output(self, expand: bool = False) -> sp.Expr:
        if self.u_unexpanded is None:
            raise RuntimeError("network not built")
        return sp.expand(self.u_unexpanded) if expand else self.u_unexpanded

    def derivatives(self, expand: bool = False) -> dict[str, sp.Expr]:
        if self.widths == [2, 1]:
            node = self.layers[0][0]
            u_x = sp.Symbol("c1") * node.h_x
            u_t = sp.Symbol("c1") * node.h_t
            u_xxx = sp.Symbol("c1") * node.h_xxx
        else:
            out_nodes = self.layers[-1]
            u_x = sum(self.output_weights[i] * n.h_x for i, n in enumerate(out_nodes))
            u_t = sum(self.output_weights[i] * n.h_t for i, n in enumerate(out_nodes))
            u_xxx = sum(self.output_weights[i] * n.h_xxx for i, n in enumerate(out_nodes))
        values = {
            "u": self.output(expand=expand),
            "u_x": sp.expand(u_x) if expand else u_x,
            "u_t": sp.expand(u_t) if expand else u_t,
            "u_xxx": sp.expand(u_xxx) if expand else u_xxx,
        }
        return values

    def residual(self, expand: bool = False) -> sp.Expr:
        d = self.derivatives(expand=False)
        residual = d["u_t"] + d["u"] * d["u_x"] + d["u"] ** 2 * d["u_x"] + d["u_xxx"]
        return sp.expand(residual) if expand else residual

    def stats(self) -> dict:
        lazy = self.derivatives(expand=False)
        expanded = self.derivatives(expand=True)
        unique_subexprs = len({sp.srepr(node.h) for node in self.nodes.values()})
        unique_derivative_subexprs = len(
            {sp.srepr(expr) for node in self.nodes.values() for expr in
             (node.h, node.h_x, node.h_t, node.h_xx, node.h_xxx)}
        )
        return {
            "widths": self.widths,
            "node_count": len(self.nodes),
            "hidden_node_count": sum(len(layer) for layer in self.layers),
            "unique_h_subexprs": unique_subexprs,
            "unique_derivative_subexprs": unique_derivative_subexprs,
            "lazy_u_ops": sp.count_ops(lazy["u"]),
            "expanded_u_ops": sp.count_ops(expanded["u"]),
            "lazy_u_xxx_ops": sp.count_ops(lazy["u_xxx"]),
            "expanded_u_xxx_ops": sp.count_ops(expanded["u_xxx"]),
            "lazy_u_length": len(sp.sstr(lazy["u"])),
            "expanded_u_length": len(sp.sstr(expanded["u"])),
            "lazy_u_xxx_length": len(sp.sstr(lazy["u_xxx"])),
            "expanded_u_xxx_length": len(sp.sstr(expanded["u_xxx"])),
            "lazy_residual_ops": sp.count_ops(self.residual(expand=False)),
            "expanded_residual_ops": sp.count_ops(self.residual(expand=True)),
        }


def make_activation(expr: str):
    return sfg._sympify_f(expr)
