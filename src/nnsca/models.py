"""Data model for bounded SFG-generated NNSCA network structures."""

from __future__ import annotations

from dataclasses import dataclass, field

import sympy as sp

from sfg.atoms import ActivationAtom, parse_activation

from .registry import (
    ROLE_INPUT_COEFFICIENT,
    ROLE_NODE_BIAS,
    ROLE_NODE_WEIGHT,
    ROLE_OUTPUT_BIAS,
    ROLE_OUTPUT_WEIGHT,
    ROLE_SPECIAL_FUNCTION_PARAMETER,
    ParameterRegistry,
)

X = sp.symbols("x", real=True)
T = sp.symbols("t", real=True)


@dataclass(frozen=True)
class NetworkConnection:
    source: str
    target: str
    weight: sp.Symbol

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "target": self.target,
            "weight": str(self.weight),
        }


@dataclass
class NetworkNode:
    node_id: str
    layer: int
    index: int
    activation: ActivationAtom | None
    source_ids: tuple[str, ...] = ()
    bias: sp.Symbol | None = None

    @property
    def is_input(self) -> bool:
        return self.layer == 0

    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "layer": self.layer,
            "index": self.index,
            "activation": self.activation.to_dict() if self.activation is not None else None,
            "source_ids": list(self.source_ids),
            "bias": str(self.bias) if self.bias is not None else None,
        }


@dataclass(frozen=True)
class OutputTerm:
    node_id: str
    weight: sp.Symbol


@dataclass
class NetworkStructure:
    """A complete, traceable NNSCA topology.

    Hidden nodes are activated by independently chosen atoms.  Connections are
    explicit, so sparse and skip connections are first-class rather than a
    hidden convention of a fixed layer constructor.
    """

    structure_id: str
    nodes: dict[str, NetworkNode] = field(default_factory=dict)
    connections: list[NetworkConnection] = field(default_factory=list)
    output_terms: list[OutputTerm] = field(default_factory=list)
    output_bias: sp.Symbol = field(default_factory=lambda: sp.Symbol("c0"))
    registry: ParameterRegistry = field(default_factory=ParameterRegistry)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.nodes:
            return
        for node in self.nodes.values():
            if node.is_input:
                continue
            if node.activation is None:
                raise ValueError(f"hidden node {node.node_id} has no activation")
            for source in node.source_ids:
                if source not in self.nodes:
                    raise ValueError(
                        f"node {node.node_id} references missing source {source!r}"
                    )
        output_nodes = {term.node_id for term in self.output_terms}
        for node_id in output_nodes:
            if node_id not in self.nodes:
                raise ValueError(f"output references missing node {node_id!r}")

    @classmethod
    def from_layers(
        cls,
        widths: list[int],
        activations: list[ActivationAtom | str | sp.Basic] | None = None,
        sparse: bool = False,
        structure_id: str | None = None,
    ) -> "NetworkStructure":
        """Compatibility constructor for layered networks.

        The first width must be the number of input coordinates and the last
        width is the number of output terms.  This remains a convenience
        constructor; the new core is the explicit node/connection model.
        """
        if len(widths) < 2:
            raise ValueError("widths must contain input and output widths")
        input_width = int(widths[0])
        output_width = int(widths[-1])
        hidden_widths = [int(w) for w in widths[1:-1]]
        activations = list(activations or [])

        structure = cls(structure_id or "layered", nodes={})
        structure.output_bias = sp.Symbol("b_out")
        input_names = [f"x{i}" for i in range(input_width)]
        for index, name in enumerate(input_names):
            structure.nodes[name] = NetworkNode(name, 0, index, None)

        total_hidden = sum(hidden_widths)
        atoms: list[ActivationAtom] = []
        for index in range(total_hidden):
            raw = activations[index] if index < len(activations) else "tanh"
            atoms.append(parse_activation(raw))

        previous = list(input_names)
        cursor = 0
        output_candidates: list[str] = []
        for layer_idx, width in enumerate(hidden_widths, start=1):
            current: list[str] = []
            for node_idx in range(width):
                atom = atoms[cursor]
                cursor += 1
                node_id = f"h{layer_idx}_{node_idx}"
                bias = structure.registry.register(ROLE_NODE_BIAS, f"b{layer_idx}_{node_idx}")
                structure.nodes[node_id] = NetworkNode(node_id, layer_idx, node_idx, atom, tuple(previous), bias)
                for source_idx, source in enumerate(previous):
                    weight = structure.registry.register(
                        ROLE_NODE_WEIGHT, f"w{layer_idx}_{node_idx}_{source_idx}"
                    )
                    structure.connections.append(NetworkConnection(source, node_id, weight))
                current.append(node_id)
            previous = current
            output_candidates = current

        structure.output_terms = []
        for out_idx in range(output_width):
            target = output_candidates[out_idx] if out_idx < len(output_candidates) else output_candidates[0]
            weight = structure.registry.register(ROLE_OUTPUT_WEIGHT, f"w_out_{out_idx}")
            structure.output_terms.append(OutputTerm(target, weight))
        structure._validate()
        return structure

    def add_hidden_node(
        self,
        node_id: str,
        layer: int,
        index: int,
        activation: ActivationAtom | str,
        source_ids: list[str],
    ) -> "NetworkStructure":
        atom = parse_activation(activation)
        bias = self.registry.register(ROLE_NODE_BIAS, f"b{layer}_{index}")
        node = NetworkNode(node_id, layer, index, atom, tuple(source_ids), bias)
        self.nodes[node_id] = node
        for source_idx, source in enumerate(source_ids):
            weight = self.registry.register(ROLE_NODE_WEIGHT, f"w{layer}_{index}_{source_idx}")
            self.connections.append(NetworkConnection(source, node_id, weight))
        self._validate()
        return self

    def set_linear_output(self, node_ids: list[str]) -> "NetworkStructure":
        self.output_terms = []
        for out_idx, node_id in enumerate(node_ids):
            weight = self.registry.register(ROLE_OUTPUT_WEIGHT, f"w_out_{out_idx}")
            self.output_terms.append(OutputTerm(node_id, weight))
        self._validate()
        return self

    def hidden_nodes(self) -> list[NetworkNode]:
        return [node for node in self.nodes.values() if not node.is_input]

    def input_nodes(self) -> list[NetworkNode]:
        return [node for node in self.nodes.values() if node.is_input]

    @staticmethod
    def special_parameter_symbol(parameter: sp.Symbol, node_id: str) -> sp.Symbol:
        """Node-scoped copy of an atom-level special parameter."""
        return sp.Symbol(f"{parameter}_{node_id}")

    def unknown_parameters(self) -> list[sp.Symbol]:
        symbols: list[sp.Symbol] = []
        for node in self.hidden_nodes():
            if node.bias is not None:
                symbols.append(node.bias)
            if node.activation is not None:
                symbols.extend(
                    self.special_parameter_symbol(param, node.node_id)
                    for param in node.activation.parameter_symbols
                )
        symbols.extend(connection.weight for connection in self.connections)
        symbols.extend(term.weight for term in self.output_terms)
        symbols.append(self.output_bias)
        unique: dict[str, sp.Symbol] = {}
        for symbol in symbols:
            if symbol is not None:
                unique[str(symbol)] = symbol
        return [unique[name] for name in sorted(unique)]

    def parameter_roles(self) -> dict[str, list[str]]:
        roles: dict[str, list[str]] = {}
        for symbol in self.unknown_parameters():
            role = self.registry.role_of(symbol) or self._infer_role(symbol)
            roles.setdefault(role, []).append(str(symbol))
        return roles

    @staticmethod
    def _infer_role(symbol: sp.Symbol) -> str:
        name = str(symbol)
        if name == "c0" or name == "b_out" or name == "d":
            return ROLE_OUTPUT_BIAS
        if name.startswith("w_out") or name == "c1":
            return ROLE_OUTPUT_WEIGHT
        if name.startswith("b"):
            return ROLE_NODE_BIAS
        if name.startswith("w"):
            return ROLE_NODE_WEIGHT
        return ROLE_SPECIAL_FUNCTION_PARAMETER

    def activation_functions(self) -> dict[str, dict]:
        return {
            node.node_id: node.activation.to_dict()
            for node in self.hidden_nodes()
            if node.activation is not None
        }

    def signature(self) -> str:
        node_parts = []
        for node in self.nodes.values():
            activation = node.activation.name if node.activation is not None else "input"
            node_parts.append(
                f"{node.node_id}:{node.layer}:{node.index}:{activation}:"
                f"{','.join(sorted(node.source_ids))}"
            )
        connections = sorted(
            (connection.source, connection.target, str(connection.weight))
            for connection in self.connections
        )
        output = sorted(
            (term.node_id, str(term.weight)) for term in self.output_terms
        )
        return "|".join(sorted(node_parts) + [str(connections), str(output)])

    def to_dict(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "nodes": {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            "connections": [connection.to_dict() for connection in self.connections],
            "output_bias": str(self.output_bias),
            "output_terms": [
                {"node_id": term.node_id, "weight": str(term.weight)}
                for term in self.output_terms
            ],
            "unknown_parameters": [str(s) for s in self.unknown_parameters()],
            "parameter_roles": self.parameter_roles(),
            "metadata": self.metadata,
        }


@dataclass
class AnsatzCandidate:
    candidate_id: str
    structure: NetworkStructure
    expression: sp.Expr | None = None
    unknown_parameters: list[sp.Symbol] = field(default_factory=list)
    activation_functions: dict = field(default_factory=dict)
    parameter_roles: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "structure": self.structure.to_dict(),
            "expression": sp.sstr(self.expression) if self.expression is not None else None,
            "unknown_parameters": [str(s) for s in self.unknown_parameters],
            "activation_functions": self.activation_functions,
            "parameter_roles": self.parameter_roles,
            "metadata": self.metadata,
        }
