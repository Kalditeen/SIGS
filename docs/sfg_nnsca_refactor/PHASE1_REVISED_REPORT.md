# SFG-NNSCA Phase 1 Revised Report

This report covers the revised Phase 1 task based on the validated NNSCA
paper architectures.

## Phase 1-A: Paper Architecture Organization

Created [PAPER_NETWORK_ARCHITECTURES.md](/Users/kang/SIGS/docs/sfg_nnsca_refactor/PAPER_NETWORK_ARCHITECTURES.md)
with the five framework computation graphs:

- Framework (2-3-1)-1
- Framework (2-2-3-1)-1
- Framework (2-3-2-1)-3
- Framework (2-2-2-1)-2
- Framework (2-3-2-1-1)-1

Each entry documents input phases, activation nodes, connection weights,
node biases, and the output expression.  The builders in
`src/sfg/paper_templates.py` are the executable version of the same graphs.

## Phase 1-B: Network IR and Activation Registry

Added:

- `src/sfg/network_ir.py`
- `src/sfg/activation_registry.py`

The IR supports independent phase nodes, node-scoped activations, sparse and
skip edges, a unified output layer, serialization, topological validation, and
parameter-role tracking.

The activation registry covers identity, square, exp, log, sin, cos, tanh,
sech, sinh, cosh, JacobiSN, JacobiCN, and JacobiDN.  Jacobi functions are
first-class entries with their modulus-square parameter `m`.

## Phase 1-C: Ansatz Compiler

Added:

- `src/nnsca/compiler/__init__.py`
- `src/nnsca/compiler/ansatz_compiler.py`

The compiler accepts either the new `NetworkIR` or the legacy
`NetworkStructure`, computes general mixed derivatives, and returns
`CompiledAnsatz` with parameter roles and network metadata preserved.

Five paper-template compilation regressions were added in
`tests/test_paper_architectures.py`.  Each template is compared against a
manually written SymPy expression.

## Phase 1-D: Mixed Derivatives and Stage2 Adapter

`CompiledAnsatz.derivative(...)` supports arbitrary mixed orders, including
`u_xxx` and `u_xxt`.  `src/nnsca/adapter.py` now exposes `Stage2Input` and
keeps the existing `Stage2Adapter` as the thin bridge into Stage2.

## Phase 1-E: Effective Network Analysis

Added:

- `src/nnsca/analysis/effective_network.py`

It identifies zero-weight edges, inactive output terms, unreachable nodes,
and classifies the constrained network as `EXACT_TRIVIAL`,
`EXACT_SINGLE_NODE`, `EXACT_DEGENERATE_MULTI_NODE`, or
`EXACT_NONDEGENERATE_MULTI_NODE`.  The original IR is never mutated.

## Phase 1-F: CH and Gardner Compatibility

Added `tests/test_paper_ch_gardner.py`:

- All five paper templates compile for Gardner and Camassa-Holm residuals.
- `Stage2Input` preserves candidate id, parameter roles, and structure trace.
- The known Gardner JacobiCN branch is used only as an external regression
  benchmark, not as solver input.

## Test Results

```text
python3 -m pytest tests/test_paper_architectures.py \
  tests/test_effective_network.py \
  tests/test_paper_ch_gardner.py -q
# 16 passed
```

```text
python3 -m pytest tests/test_sfg_nnsca_refactor.py \
  tests/test_sfg_bbm_21.py tests/test_sfg_gardner.py -q
# 59 passed
```

```text
python3 -m pytest tests/test_sfg_gardner_phase2.py \
  tests/test_sfg_gardner_phase3.py \
  tests/test_sfg_gardner_phase4.py -q
# 33 passed
```

```text
PYTHONPATH=src python3 -m pytest tests -q --ignore=tests/test_hf_data.py
# 121 passed
```

Full-suite collection still has the pre-existing
`pyarrow requires NumPy 2.0 or newer, found 1.26.4` environment failure in
`tests/test_hf_data.py`.

## Milestone

`PAPER_ARCHITECTURE_COMPILER_MILESTONE_PASSED`

All architecture, compiler, effective-network, CH, and Gardner compatibility
requirements in this revised Phase 1 are implemented and passing in the
environment excluding the known unrelated `test_hf_data.py` dependency issue.
