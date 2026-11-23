#!/usr/bin/env python3
"""Layered symbolic network graph for Gardner phase 3.

This is a small computation-graph implementation.  It keeps intermediate
activation expressions and their cached spatial/time derivatives instead of
substituting one fully nested expression.  It is used for comparison with
direct SymPy differentiation, not as a replacement for the existing SFG
verification gate.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import sympy as sp

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
PDES_DIR = REPO_ROOT / "scripts" / "pdes"
for path in (SRC_DIR, PDES_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import sfg_bbm_21 as sfg  # noqa: E402

X, T = sfg.X, sfg.T
Z = sfg.Z


@dataclass
class NodeValues:
    z: sp.Expr
    h: sp.Expr
    h_x: sp.Expr
    h_t: sp.Expr
    h_xx: sp.Expr
    h_xxx: sp.Expr


class LayeredNetwork:
    def __init__(self, widths, activation=None):
        self.widths = list(widths)
        self.activation = activation if activation is not None else sp.tanh(Z)
        if len(self.widths) < 2 or self.widths[0] != 2 or self.widths[-1] != 1:
            raise ValueError("widths must start with 2 and end with 1")

    def _activation_derivatives(self, z_expr: sp.Expr):
        f = self.activation
        fz = f.subs(Z, z_expr)
        fp_expr = sp.diff(f, Z)
        fpp_expr = sp.diff(f, Z, 2)
        fppp_expr = sp.diff(f, Z, 3)
        return (
            fz,
            fp_expr.subs(Z, z_expr),
            fpp_expr.subs(Z, z_expr),
            fppp_expr.subs(Z, z_expr),
        )

    def build(self) -> tuple[list[list[NodeValues]], sp.Expr]:
        hidden = self.widths[1:-1]
        if self.widths == [2, 1]:
            a = sp.Symbol("a")
            b = sp.Symbol("b")
            d = sp.Symbol("d")
            z_expr = a * X + b * T + d
            fz, fp, fpp, fppp = self._activation_derivatives(z_expr)
            node = NodeValues(z_expr, fz, fp * a, fp * b, fpp * a**2, fppp * a**3)
            u = sp.Symbol("c0") + sp.Symbol("c1") * fz
            return [[node]], sp.expand(u)
        previous = [
            NodeValues(X, X, sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(0)),
            NodeValues(T, T, sp.Integer(0), sp.Integer(1), sp.Integer(0), sp.Integer(0)),
        ]
        layers: list[list[NodeValues]] = []
        for layer_idx, width in enumerate(hidden):
            current: list[NodeValues] = []
            for node_idx in range(width):
                z_expr = sp.Symbol(f"b{layer_idx + 1}_{node_idx}")
                z_x = sp.Integer(0)
                z_t = sp.Integer(0)
                z_xx = sp.Integer(0)
                z_xxx = sp.Integer(0)
                for input_idx, node in enumerate(previous):
                    w = sp.Symbol(f"w{layer_idx + 1}_{node_idx}_{input_idx}")
                    z_expr += w * node.h
                    z_x += w * node.h_x
                    z_t += w * node.h_t
                    z_xx += w * node.h_xx
                    z_xxx += w * node.h_xxx
                fz, fp, fpp, fppp = self._activation_derivatives(z_expr)
                h_x = fp * z_x
                h_t = fp * z_t
                h_xx = fpp * z_x**2 + fp * z_xx
                h_xxx = fppp * z_x**3 + 3 * fpp * z_x * z_xx + fp * z_xxx
                current.append(NodeValues(z_expr, fz, h_x, h_t, h_xx, h_xxx))
            layers.append(current)
            previous = current

        u = sp.Symbol("b_out")
        for node_idx, node in enumerate(layers[-1]):
            w = sp.Symbol(f"w_out_{node_idx}")
            u += w * node.h
        return layers, sp.expand(u)

    def derivatives(self) -> dict[str, sp.Expr]:
        layers, u = self.build()
        if self.widths == [2, 1]:
            node = layers[0][0]
            c1 = sp.Symbol("c1")
            return {
                "u": u,
                "u_x": sp.expand(c1 * node.h_x),
                "u_t": sp.expand(c1 * node.h_t),
                "u_xxx": sp.expand(c1 * node.h_xxx),
            }
        u_x = sum(sp.Symbol(f"w_out_{i}") * n.h_x for i, n in enumerate(layers[-1]))
        u_t = sum(sp.Symbol(f"w_out_{i}") * n.h_t for i, n in enumerate(layers[-1]))
        u_xxx = sum(sp.Symbol(f"w_out_{i}") * n.h_xxx for i, n in enumerate(layers[-1]))
        return {"u": u, "u_x": sp.expand(u_x), "u_t": sp.expand(u_t), "u_xxx": sp.expand(u_xxx)}

    def stats(self) -> dict:
        layers, u = self.build()
        derivative_map = self.derivatives()
        return {
            "widths": self.widths,
            "node_count": sum(len(layer) for layer in layers),
            "u_ops": sp.count_ops(u),
            "u_x_ops": sp.count_ops(derivative_map["u_x"]),
            "u_t_ops": sp.count_ops(derivative_map["u_t"]),
            "u_xxx_ops": sp.count_ops(derivative_map["u_xxx"]),
            "u_length": len(sp.sstr(u)),
            "u_xxx_length": len(sp.sstr(derivative_map["u_xxx"])),
        }


def direct_network_trial(widths, activation=None):
    activation = activation if activation is not None else sp.tanh(Z)
    return sfg.build_trial(activation, widths)
