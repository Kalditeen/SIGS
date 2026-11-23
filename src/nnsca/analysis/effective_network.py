"""Analyse the effective network after symbolic parameter constraints."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from sfg.network_ir import NetworkIR


@dataclass
class EffectiveNetworkResult:
    original_ir_id: str
    effective_edges: list[str]
    inactive_edges: list[str]
    active_outputs: list[str]
    inactive_outputs: list[str]
    active_nodes: list[str]
    unreachable_nodes: list[str]
    reduced_expression: str | None
    classification: str
    reasons: list[str]

    def to_dict(self) -> dict:
        return {
            "original_ir_id": self.original_ir_id,
            "effective_edges": self.effective_edges,
            "inactive_edges": self.inactive_edges,
            "active_outputs": self.active_outputs,
            "inactive_outputs": self.inactive_outputs,
            "active_nodes": self.active_nodes,
            "unreachable_nodes": self.unreachable_nodes,
            "reduced_expression": self.reduced_expression,
            "classification": self.classification,
            "reasons": self.reasons,
        }


def _evaluate(symbol: sp.Symbol, constraints: dict[sp.Symbol, sp.Expr] | dict[str, str]) -> sp.Expr:
    if isinstance(constraints, dict):
        for key, value in constraints.items():
            if isinstance(key, sp.Symbol) and key == symbol:
                return sp.sympify(value)
            if str(key) == str(symbol):
                return sp.sympify(value)
    return symbol


def analyze_effective_network(
    ir: NetworkIR,
    constraints: dict[sp.Symbol, sp.Expr] | dict[str, str],
    compiler=None,
) -> EffectiveNetworkResult:
    """Return structural-degeneration information without modifying ``ir``."""

    effective_edges: list[str] = []
    inactive_edges: list[str] = []
    for edge in ir.edges.values():
        value = sp.expand(_evaluate(edge.weight, constraints))
        if value == 0:
            inactive_edges.append(edge.edge_id)
        else:
            effective_edges.append(edge.edge_id)

    active_outputs: list[str] = []
    inactive_outputs: list[str] = []
    for term in ir.output_terms:
        value = sp.expand(_evaluate(term.weight, constraints))
        if value == 0:
            inactive_outputs.append(term.source)
        else:
            active_outputs.append(term.source)

    reachable = set(active_outputs)
    changed = True
    while changed:
        changed = False
        for edge in ir.edges.values():
            if edge.edge_id in effective_edges and edge.target in reachable and edge.source not in reachable:
                reachable.add(edge.source)
                changed = True

    active_nodes = sorted(node_id for node_id in ir.nodes if node_id in reachable)
    unreachable_nodes = sorted(node_id for node_id in ir.nodes if node_id not in reachable)

    reduced_expression = None
    if compiler is not None and constraints:
        candidate = compiler.compile_ir(ir)
        clean: dict[sp.Symbol, sp.Expr] = {}
        for symbol, value in constraints.items():
            if isinstance(symbol, str):
                clean[sp.Symbol(symbol)] = sp.sympify(value)
            else:
                clean[symbol] = value
        try:
            reduced_expression = sp.sstr(sp.expand(candidate.expression.subs(clean)))
        except Exception:
            reduced_expression = None

    if not active_outputs:
        classification = "EXACT_TRIVIAL"
    elif len(active_outputs) == 1:
        classification = "EXACT_SINGLE_NODE"
    elif len(active_nodes) < len(ir.nodes):
        classification = "EXACT_DEGENERATE_MULTI_NODE"
    else:
        classification = "EXACT_NONDEGENERATE_MULTI_NODE"

    reasons: list[str] = []
    if inactive_edges:
        reasons.append(f"{len(inactive_edges)} zero-weight connections deactivated")
    if unreachable_nodes:
        reasons.append(f"{len(unreachable_nodes)} nodes do not reach the output")
    if inactive_outputs:
        reasons.append(f"{len(inactive_outputs)} output terms have zero weight")

    return EffectiveNetworkResult(
        original_ir_id=ir.ir_id,
        effective_edges=effective_edges,
        inactive_edges=inactive_edges,
        active_outputs=active_outputs,
        inactive_outputs=inactive_outputs,
        active_nodes=active_nodes,
        unreachable_nodes=unreachable_nodes,
        reduced_expression=reduced_expression,
        classification=classification,
        reasons=reasons,
    )
