# Phase 2 Interface Audit

This audit records the actual Phase 1 interfaces used by Phase 2.  It was
derived from the source files listed below, not from older design documents.

Audited files:

- `src/sfg/network_ir.py`
- `src/sfg/activation_registry.py`
- `src/sfg/paper_templates.py`
- `src/nnsca/compiler/ansatz_compiler.py`
- `src/nnsca/analysis/effective_network.py`
- `src/nnsca/adapter.py`
- `src/nnsca/models.py`

## NetworkIR

`NetworkIR` is a mutable dataclass with these fields:

- `ir_id: str`
- `phases: dict[str, PhaseNode]`
- `nodes: dict[str, ComputeNode]`
- `edges: dict[tuple[str, str], Edge]`
- `output_terms: list[OutputTerm]`
- `output_bias: sp.Symbol`
- `metadata: dict`

Useful construction methods:

- `add_phase(node_id, x_weight=None, t_weight=None, bias=None)`
- `add_compute(node_id, activation, sources, bias=None)`
- `set_linear_output(sources, output_bias=None)`

`add_compute` automatically creates one `Edge` per source.  Validation is run
after every construction call and on `from_dict`.

Other relevant methods:

- `validate()`
- `topological_order()`
- `parameter_symbols()`
- `parameter_roles()`
- `activation_functions()`
- `signature()`
- `to_dict()` / `from_dict()`

Nodes do not carry an explicit layer field.  Layer is therefore inferred from
source depth by the Phase 2 helper `sfg.architecture_utils.infer_layers`.

## Activation Registry

`activation_by_name(name)` returns an `ActivationSpec`.  `available_activations()`
returns every registered spec.  A spec exposes:

- `name`
- `family`
- `expression`
- `parameter_names`
- `parameter_roles`
- `domain`
- `differentiable`
- `instantiate(preactivation)`
- `derivative(order=1)`

Jacobi activations use `m` as their internal parameter and are scoped per node
by the compiler.

## Paper Templates

`PAPER_TEMPLATES` maps names to builder functions:

- `231`
- `2231`
- `2321`
- `2221`
- `23211`

`paper_templates()` returns a fresh `NetworkIR` for each template.  Template
IRs carry `metadata["source"] == "paper_architecture_template"`.

## AnsatzCompiler

`AnsatzCompiler.compile_ir(ir, expand=False)` returns `CompiledAnsatz`.
`CompiledAnsatz` exposes:

- `candidate`
- `expression`
- `derivative(*orders)`
- `partial(symbol, order=1)`
- `to_dict()`

The compiler supports both revised `NetworkIR` and legacy `NetworkStructure`.

## Effective Network Analysis

`analyze_effective_network(ir, constraints, compiler=None)` returns
`EffectiveNetworkResult` with effective/inactive edges, active/inactive
outputs, active/unreachable nodes, reduced expression, classification, and
reasons.  It does not mutate the original IR.

## Stage2Input

`Stage2Input` is a thin dataclass carrying PDE, expression, unknown
parameters, roles, candidate id, and optional structure trace.  Phase 2 does
not invoke Stage2.

## Reusable Modules

Phase 2 reuses:

- `NetworkIR` for all candidate representation
- `activation_by_name` / `available_activations` for node-scoped activation
- `PAPER_TEMPLATES` for seed candidates
- `AnsatzCompiler` for compilation
- `NetworkIR.to_dict` / `from_dict` for persistence

## Required Extensions

Phase 2 adds:

- centralized generation bounds
- paper-template derivation
- node/connection/depth mutation
- canonical structural signatures
- candidate management, deduplication, persistence, and statistics
- deterministic experiment entry point

No existing Phase 1 interface needed modification for Phase 2.
