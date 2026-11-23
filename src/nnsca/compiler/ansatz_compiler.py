"""Canonical AnsatzCompiler for the revised Network IR."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from nnsca.models import AnsatzCandidate, NetworkStructure, X, T
from sfg.network_ir import NetworkIR


@dataclass
class CompiledAnsatz:
    candidate: AnsatzCandidate
    expression: sp.Expr
    derivative_cache: dict

    def derivative(self, *orders: tuple[sp.Symbol, int]) -> sp.Expr:
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
    """Compile either a legacy NetworkStructure or a revised NetworkIR."""

    def compile(self, candidate: AnsatzCandidate, expand: bool = False) -> CompiledAnsatz:
        if candidate.network_ir is not None:
            expression = self._compile_ir(candidate.network_ir, expand=expand)
            ir = candidate.network_ir
            candidate.expression = expression
            candidate.unknown_parameters = ir.parameter_symbols()
            candidate.activation_functions = {
                node.node_id: node.activation.name
                for node in ir.nodes.values()
            }
            candidate.parameter_roles = ir.parameter_roles()
            candidate.metadata.setdefault("network_ir", ir.to_dict())
            return CompiledAnsatz(candidate, expression, {})

        if candidate.structure is None:
            raise ValueError("candidate must contain a structure or network_ir")
        expression = self._compile_structure(candidate.structure, expand=expand)
        candidate.expression = expression
        candidate.unknown_parameters = candidate.structure.unknown_parameters()
        candidate.activation_functions = candidate.structure.activation_functions()
        candidate.parameter_roles = candidate.structure.parameter_roles()
        return CompiledAnsatz(candidate, expression, {})

    def compile_ir(self, ir: NetworkIR, expand: bool = False) -> CompiledAnsatz:
        candidate = AnsatzCandidate(
            candidate_id=ir.ir_id,
            structure=None,
            network_ir=ir,
        )
        return self.compile(candidate, expand=expand)

    def _compile_ir(self, ir: NetworkIR, expand: bool = False) -> sp.Expr:
        values: dict[str, sp.Expr] = {}
        for phase in ir.phases.values():
            values[phase.node_id] = (
                phase.x_weight * X + phase.t_weight * T + phase.bias
            )

        for node_id in ir.topological_order():
            node = ir.nodes[node_id]
            preactivation = node.bias
            for source in node.sources:
                edge = ir.edges[(source, node_id)]
                preactivation += edge.weight * values[source]
            activated = node.activation.instantiate(preactivation)
            for param_name in node.activation.parameter_names:
                scoped = sp.Symbol(f"{param_name}_{node_id}")
                activated = activated.subs(sp.Symbol(param_name), scoped)
            values[node_id] = activated

        output = ir.output_bias
        for term in ir.output_terms:
            output += term.weight * values[term.source]
        return sp.expand(output) if expand else output

    def _compile_structure(self, structure: NetworkStructure, expand: bool = False) -> sp.Expr:
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
                    raise ValueError(f"missing connection weight for {source_id} -> {node.node_id}")
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
        return sp.expand(output) if expand else output

    def compile_structure(self, structure: NetworkStructure, expand: bool = False) -> CompiledAnsatz:
        candidate = AnsatzCandidate(
            candidate_id=structure.structure_id,
            structure=structure,
        )
        return self.compile(candidate, expand=expand)
