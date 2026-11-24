"""Network IR adaptation and symbolic compilation for Phase 1.5.

The IR is intentionally a small, reviewable DAG rather than a final SymPy
expression.  LLM prompts can be built from ``topology_summary`` without first
expanding the network, as required by the experiment design.
"""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass, field

import sympy as sp

from . import ch_equation as ce

INPUT_OP = "input"
CONST_OP = "const"
AFFINE_OP = "affine"
ACTIVATION_OP = "activation"
ADD_OP = "add"
MUL_OP = "mul"


@dataclass
class NetworkIR:
    network_id: str
    level: int
    signature: str
    input_vars: list[str]
    parameters: list[str]
    nodes: list[dict]
    output_node: str
    reference: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "network_id": self.network_id,
            "level": self.level,
            "signature": self.signature,
            "input_vars": list(self.input_vars),
            "parameters": list(self.parameters),
            "nodes": [dict(node) for node in self.nodes],
            "output_node": self.output_node,
            "reference": dict(self.reference),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "NetworkIR":
        return cls(
            network_id=data["network_id"],
            level=int(data["level"]),
            signature=data["signature"],
            input_vars=list(data["input_vars"]),
            parameters=list(data["parameters"]),
            nodes=[dict(node) for node in data["nodes"]],
            output_node=data["output_node"],
            reference=dict(data.get("reference", {})),
        )


def _symbols_for(ir: NetworkIR) -> dict[str, sp.Symbol]:
    """Create one stable SymPy symbol per declared parameter name."""
    symbols: dict[str, sp.Symbol] = {"x": ce.X, "t": ce.T}
    for name in ir.parameters:
        symbols[name] = sp.Symbol(name)
    return symbols


def node_by_id(ir: NetworkIR) -> dict[str, dict]:
    return {node["id"]: node for node in ir.nodes}


def topological_order(ir: NetworkIR) -> list[dict]:
    """Return nodes in an executable order, raising on cycles or bad refs."""
    nodes = node_by_id(ir)
    resolved: set[str] = set(ir.input_vars)
    unresolved = deque(nodes.values())
    ordered: list[dict] = []
    progress = True
    while unresolved and progress:
        progress = False
        for _ in range(len(unresolved)):
            node = unresolved.popleft()
            inputs = node.get("inputs", [])
            if all(input_id in resolved for input_id in inputs):
                ordered.append(node)
                resolved.add(node["id"])
                progress = True
            else:
                unresolved.append(node)
    if unresolved:
        missing = [node["id"] for node in unresolved]
        raise ValueError(f"network has cyclic or unknown inputs: {missing}")
    return ordered


def _compile_node(
    node: dict,
    env: dict[str, sp.Expr],
    symbols: dict[str, sp.Symbol],
    activation_registry,
) -> sp.Expr:
    op = node.get("op")
    if op == INPUT_OP:
        return symbols[node.get("symbol", node["id"])]
    if op == CONST_OP:
        return sp.sympify(node["value"])
    if op == AFFINE_OP:
        total = sp.Integer(0)
        coeffs = node.get("coeffs", {})
        for input_id in node.get("inputs", []):
            coeff = sp.sympify(coeffs.get(input_id, "0"))
            total = sp.expand(total + coeff * env[input_id])
        if "bias" in node:
            total = sp.expand(total + sp.sympify(node["bias"]))
        return sp.expand(total)
    if op == ACTIVATION_OP:
        inputs = node.get("inputs", [])
        if len(inputs) != 1:
            raise ValueError(f"activation node {node['id']} must have one input")
        return activation_registry.apply(node["activation"], env[inputs[0]])
    if op == ADD_OP:
        return sp.expand(sp.Add(*[env[input_id] for input_id in node.get("inputs", [])]))
    if op == MUL_OP:
        result = sp.Integer(1)
        for input_id in node.get("inputs", []):
            result = sp.expand(result * env[input_id])
        return sp.expand(result)
    raise ValueError(f"unsupported node op {op!r} in node {node['id']}")


def compile_expression(ir: NetworkIR, activation_registry) -> sp.Expr:
    """Compile an IR into a SymPy expression and an intermediate map."""
    symbols = _symbols_for(ir)
    env: dict[str, sp.Expr] = {"x": symbols["x"], "t": symbols["t"]}
    intermediates: dict[str, sp.Expr] = {"x": symbols["x"], "t": symbols["t"]}
    for node in topological_order(ir):
        expression = _compile_node(node, env, symbols, activation_registry)
        env[node["id"]] = expression
        intermediates[node["id"]] = expression
    if ir.output_node not in env:
        raise ValueError(f"output node {ir.output_node!r} is missing from IR")
    return sp.expand(env[ir.output_node])


def consumer_counts(ir: NetworkIR) -> Counter:
    counts: Counter = Counter()
    for node in ir.nodes:
        for input_id in node.get("inputs", []):
            counts[input_id] += 1
    return counts


def activation_inventory(ir: NetworkIR) -> list[str]:
    return sorted({node["activation"] for node in ir.nodes if node.get("op") == ACTIVATION_OP})


def shared_subexpressions(ir: NetworkIR) -> list[str]:
    counts = consumer_counts(ir)
    return sorted(input_id for input_id, count in counts.items() if count > 1)


def node_depth(ir: NetworkIR) -> dict[str, int]:
    nodes = node_by_id(ir)
    depths: dict[str, int] = {input_id: 0 for input_id in ir.input_vars}
    for node in topological_order(ir):
        depths[node["id"]] = 1 + max(
            (depths.get(input_id, 0) for input_id in node.get("inputs", [])),
            default=0,
        )
    return depths


def topology_summary(ir: NetworkIR) -> dict:
    """JSON-ready structural description for LLM prompts and reports."""
    depths = node_depth(ir)
    counts = consumer_counts(ir)
    return {
        "network_id": ir.network_id,
        "level": ir.level,
        "signature": ir.signature,
        "input_vars": list(ir.input_vars),
        "parameters": list(ir.parameters),
        "node_count": len(ir.nodes),
        "output_node": ir.output_node,
        "activation_inventory": activation_inventory(ir),
        "shared_subexpressions": shared_subexpressions(ir),
        "max_depth": max(depths.values(), default=0),
        "nodes": [
            {
                "id": node["id"],
                "op": node.get("op"),
                "activation": node.get("activation"),
                "inputs": node.get("inputs", []),
                "depth": depths[node["id"]],
                "consumer_count": counts[node["id"]],
            }
            for node in topological_order(ir)
        ],
    }


def _reference_network_type(level: int) -> str:
    return {
        1: "single_layer_homogeneous",
        2: "single_layer_heterogeneous",
        3: "multilayer_heterogeneous",
        4: "multibranch_hybrid",
    }.get(level, "unknown")


def reference_structure(ir: NetworkIR) -> dict:
    """Ground-truth structure from the generator, independent of any LLM."""
    summary = topology_summary(ir)
    return {
        "network_id": ir.network_id,
        "level": ir.level,
        "network_type": _reference_network_type(ir.level),
        "signature": ir.signature,
        "input_vars": list(ir.input_vars),
        "parameters": list(ir.parameters),
        "activation_inventory": summary["activation_inventory"],
        "node_count": summary["node_count"],
        "max_depth": summary["max_depth"],
        "shared_subexpressions": summary["shared_subexpressions"],
        "edges": [
            (node["id"], input_id)
            for node in ir.nodes
            for input_id in node.get("inputs", [])
        ],
    }
