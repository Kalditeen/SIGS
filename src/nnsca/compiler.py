"""Ansatz compiler: network structure -> parameterised SymPy expression."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from .models import AnsatzCandidate, NetworkStructure, X, T


@dataclass
class CompiledAnsatz:
    candidate: AnsatzCandidate
    expression: sp.Expr
    derivative_cache: dict

    def derivative(self, *orders: tuple[sp.Symbol, int]) -> sp.Expr:
        """Compute a general mixed derivative with a per-candidate cache.

        ``orders`` is a sequence of ``(symbol, order)`` pairs, e.g.
        ``((T, 1), (X, 2))`` for ``u_{xxt}``.
        """
        key = tuple((symbol, int(order)) for symbol, order in orders if int(order) > 0)
        if key in self.derivative_cache:
            return self.derivative_cache[key]
        value = self.expression
        for symbol, order in key:
            if order:
                value = sp.diff(value, symbol, order)
        self.derivative_cache[key] = value
        return value

    def partial(self, symbol: sp.Symbol, order: int = 1) -> sp.Expr:
        return self.derivative((symbol, order))

    def to_dict(self) -> dict:
        return {
            "candidate": self.candidate.to_dict(),
            "expression": sp.sstr(self.expression),
        }


class AnsatzCompiler:
    """Compile explicit SFG network structures into SymPy expressions.

    The compiler is PDE-independent and only walks the supplied graph.  It
    keeps intermediate node values for clarity, but the returned
    ``CompiledAnsatz`` caches general mixed derivatives instead of hardcoding
    ``u_t``, ``u_x``, or ``u_xxx``.
    """

    def compile(
        self,
        candidate: AnsatzCandidate,
        expand: bool = False,
    ) -> CompiledAnsatz:
        structure = candidate.structure
        values: dict[str, sp.Expr] = {}

        for node in structure.input_nodes():
            if node.index == 0:
                values[node.node_id] = X
            elif node.index == 1:
                values[node.node_id] = T
            else:
                values[node.node_id] = sp.Symbol(f"x{node.index}", real=True)

        weights = {}
        for connection in structure.connections:
            weights[(connection.target, connection.source)] = connection.weight

        for node in structure.hidden_nodes():
            preactivation = node.bias if node.bias is not None else sp.Integer(0)
            for source_id in node.source_ids:
                weight = weights.get((node.node_id, source_id))
                if weight is None:
                    raise ValueError(
                        f"missing connection weight for {source_id} -> {node.node_id}"
                    )
                preactivation += weight * values[source_id]
            if node.activation is None:
                raise ValueError(f"hidden node {node.node_id} has no activation")
            activated = node.activation.instantiate(preactivation)
            for parameter in node.activation.parameter_symbols:
                scoped = NetworkStructure.special_parameter_symbol(parameter, node.node_id)
                activated = activated.subs(parameter, scoped)
            values[node.node_id] = activated

        output = structure.output_bias
        for term in structure.output_terms:
            output += term.weight * values[term.node_id]

        expression = sp.expand(output) if expand else output
        candidate.expression = expression
        candidate.unknown_parameters = structure.unknown_parameters()
        candidate.activation_functions = structure.activation_functions()
        candidate.parameter_roles = structure.parameter_roles()
        return CompiledAnsatz(candidate, expression, {})


    def compile_structure(self, structure: NetworkStructure, expand: bool = False) -> CompiledAnsatz:
        candidate = AnsatzCandidate(
            candidate_id=structure.structure_id,
            structure=structure,
        )
        return self.compile(candidate, expand=expand)
