"""Unified Network IR for heterogeneous SFG-NNSCA computation graphs.

The IR models input phase nodes, independently activated compute nodes, sparse
or skip connections, and a unified output layer.  It deliberately does not
encode activations as a single network-wide property.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import sympy as sp

from sfg.activation_registry import ActivationSpec, parse_activation_spec

X = sp.symbols("x", real=True)
T = sp.symbols("t", real=True)

ROLE_PHASE_X = "phase_x_weight"
ROLE_PHASE_T = "phase_t_weight"
ROLE_PHASE_BIAS = "phase_bias"
ROLE_NODE_BIAS = "node_bias"
ROLE_EDGE_WEIGHT = "edge_weight"
ROLE_OUTPUT_WEIGHT = "output_weight"
ROLE_OUTPUT_BIAS = "output_bias"
ROLE_SPECIAL = "special_function_parameter"


@dataclass
class PhaseNode:
    node_id: str
    x_weight: sp.Symbol
    t_weight: sp.Symbol
    bias: sp.Symbol

    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "x_weight": str(self.x_weight),
            "t_weight": str(self.t_weight),
            "bias": str(self.bias),
        }


@dataclass
class ComputeNode:
    node_id: str
    activation: ActivationSpec
    sources: tuple[str, ...]
    bias: sp.Symbol

    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "activation": self.activation.name,
            "sources": list(self.sources),
            "bias": str(self.bias),
        }


@dataclass(frozen=True)
class Edge:
    edge_id: str
    source: str
    target: str
    weight: sp.Symbol

    def to_dict(self) -> dict:
        return {
            "edge_id": self.edge_id,
            "source": self.source,
            "target": self.target,
            "weight": str(self.weight),
        }


@dataclass(frozen=True)
class OutputTerm:
    source: str
    weight: sp.Symbol

    def to_dict(self) -> dict:
        return {"source": self.source, "weight": str(self.weight)}


@dataclass
class NetworkIR:
    """A finite DAG with independent phases, activations, and connections."""

    ir_id: str
    phases: dict[str, PhaseNode] = field(default_factory=dict)
    nodes: dict[str, ComputeNode] = field(default_factory=dict)
    edges: dict[tuple[str, str], Edge] = field(default_factory=dict)
    output_terms: list[OutputTerm] = field(default_factory=list)
    output_bias: sp.Symbol = field(default_factory=lambda: sp.Symbol("c0"))
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        for node in self.nodes.values():
            for source in node.sources:
                if source not in self.phases and source not in self.nodes:
                    raise ValueError(f"node {node.node_id} has missing source {source!r}")
                if (source, node.node_id) not in self.edges:
                    raise ValueError(f"missing edge {source} -> {node.node_id}")
        for term in self.output_terms:
            if term.source not in self.nodes and term.source not in self.phases:
                raise ValueError(f"output references missing node {term.source!r}")
        # Topological validation catches accidental cycles.
        self.topological_order()

    def add_phase(
        self,
        node_id: str,
        x_weight: str | sp.Symbol | None = None,
        t_weight: str | sp.Symbol | None = None,
        bias: str | sp.Symbol | None = None,
    ) -> "NetworkIR":
        def sym(value, default_name):
            if value is None:
                return sp.Symbol(default_name)
            return value if isinstance(value, sp.Basic) else sp.sympify(value)

        self.phases[node_id] = PhaseNode(
            node_id=node_id,
            x_weight=sym(x_weight, f"a_{node_id}"),
            t_weight=sym(t_weight, f"b_{node_id}"),
            bias=sym(bias, f"d_{node_id}"),
        )
        self.validate()
        return self

    def add_compute(
        self,
        node_id: str,
        activation: ActivationSpec | str,
        sources: list[str],
        bias: str | sp.Symbol | None = None,
    ) -> "NetworkIR":
        spec = parse_activation_spec(activation)
        bias_sym = sp.sympify(bias) if isinstance(bias, str) else bias
        if bias_sym is None:
            bias_sym = sp.Symbol(f"bias_{node_id}")
        self.nodes[node_id] = ComputeNode(
            node_id=node_id,
            activation=spec,
            sources=tuple(sources),
            bias=bias_sym,
        )
        for idx, source in enumerate(sources):
            edge_id = f"edge_{source}__{node_id}"
            self.edges[(source, node_id)] = Edge(
                edge_id=edge_id,
                source=source,
                target=node_id,
                weight=sp.Symbol(f"w_{source}__{node_id}"),
            )
        self.validate()
        return self

    def set_linear_output(
        self,
        sources: list[str],
        output_bias: str | sp.Symbol | None = None,
    ) -> "NetworkIR":
        self.output_terms = [
            OutputTerm(source=source, weight=sp.Symbol(f"c_{source}"))
            for source in sources
        ]
        if output_bias is not None:
            self.output_bias = (
                output_bias if isinstance(output_bias, sp.Basic) else sp.sympify(output_bias)
            )
        self.validate()
        return self

    def topological_order(self) -> list[str]:
        indegree: dict[str, int] = {node_id: 0 for node_id in self.nodes}
        adjacency: dict[str, list[str]] = {node_id: [] for node_id in self.nodes}
        for edge in self.edges.values():
            if edge.source in self.nodes and edge.target in self.nodes:
                adjacency[edge.source].append(edge.target)
                indegree[edge.target] += 1

        queue = sorted([node_id for node_id, degree in indegree.items() if degree == 0])
        ordered: list[str] = []
        while queue:
            current = queue.pop(0)
            ordered.append(current)
            for target in adjacency[current]:
                indegree[target] -= 1
                if indegree[target] == 0:
                    queue.append(target)
                    queue.sort()
        if len(ordered) != len(self.nodes):
            raise ValueError("NetworkIR contains a cycle")
        return ordered

    def parameter_symbols(self) -> list[sp.Symbol]:
        symbols: list[sp.Symbol] = [self.output_bias]
        for phase in self.phases.values():
            symbols.extend([phase.x_weight, phase.t_weight, phase.bias])
        for node in self.nodes.values():
            symbols.append(node.bias)
            symbols.extend(
                sp.Symbol(f"{param}_{node.node_id}")
                for param in node.activation.parameter_names
            )
        symbols.extend(edge.weight for edge in self.edges.values())
        symbols.extend(term.weight for term in self.output_terms)
        unique: dict[str, sp.Symbol] = {}
        for symbol in symbols:
            unique[str(symbol)] = symbol
        return [unique[name] for name in sorted(unique)]

    def parameter_roles(self) -> dict[str, list[str]]:
        roles: dict[str, list[str]] = {
            ROLE_PHASE_X: [],
            ROLE_PHASE_T: [],
            ROLE_PHASE_BIAS: [],
            ROLE_NODE_BIAS: [],
            ROLE_EDGE_WEIGHT: [],
            ROLE_OUTPUT_WEIGHT: [],
            ROLE_OUTPUT_BIAS: [str(self.output_bias)],
            ROLE_SPECIAL: [],
        }
        for phase in self.phases.values():
            roles[ROLE_PHASE_X].append(str(phase.x_weight))
            roles[ROLE_PHASE_T].append(str(phase.t_weight))
            roles[ROLE_PHASE_BIAS].append(str(phase.bias))
        for node in self.nodes.values():
            roles[ROLE_NODE_BIAS].append(str(node.bias))
            roles[ROLE_SPECIAL].extend(
                f"{param}_{node.node_id}" for param in node.activation.parameter_names
            )
        roles[ROLE_EDGE_WEIGHT].extend(str(edge.weight) for edge in self.edges.values())
        roles[ROLE_OUTPUT_WEIGHT].extend(str(term.weight) for term in self.output_terms)
        return {key: sorted(value) for key, value in roles.items() if value}

    def activation_functions(self) -> dict[str, str]:
        return {node.node_id: node.activation.name for node in self.nodes.values()}

    def signature(self) -> str:
        parts = []
        for phase in self.phases.values():
            parts.append(f"phase:{phase.node_id}")
        for node in self.nodes.values():
            parts.append(
                f"node:{node.node_id}:{node.activation.name}:"
                f"{','.join(sorted(node.sources))}"
            )
        edges = sorted(
            (edge.source, edge.target) for edge in self.edges.values()
        )
        outputs = sorted((term.source,) for term in self.output_terms)
        return "|".join(sorted(parts) + [str(edges), str(outputs)])

    def to_dict(self) -> dict:
        return {
            "ir_id": self.ir_id,
            "phases": [phase.to_dict() for phase in self.phases.values()],
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "edges": [edge.to_dict() for edge in self.edges.values()],
            "output_bias": str(self.output_bias),
            "output_terms": [term.to_dict() for term in self.output_terms],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "NetworkIR":
        ir = cls(ir_id=data["ir_id"])
        ir.phases = {}
        ir.nodes = {}
        ir.edges = {}
        for item in data.get("phases", []):
            ir.phases[item["node_id"]] = PhaseNode(
                node_id=item["node_id"],
                x_weight=sp.Symbol(item["x_weight"]),
                t_weight=sp.Symbol(item["t_weight"]),
                bias=sp.Symbol(item["bias"]),
            )
        for item in data.get("nodes", []):
            node = ComputeNode(
                node_id=item["node_id"],
                activation=parse_activation_spec(item["activation"]),
                sources=tuple(item["sources"]),
                bias=sp.Symbol(item["bias"]),
            )
            ir.nodes[node.node_id] = node
        for item in data.get("edges", []):
            edge = Edge(
                edge_id=item["edge_id"],
                source=item["source"],
                target=item["target"],
                weight=sp.Symbol(item["weight"]),
            )
            ir.edges[(edge.source, edge.target)] = edge
        ir.output_bias = sp.Symbol(data.get("output_bias", "c0"))
        ir.output_terms = [
            OutputTerm(source=item["source"], weight=sp.Symbol(item["weight"]))
            for item in data.get("output_terms", [])
        ]
        ir.metadata = data.get("metadata", {})
        ir.validate()
        return ir
