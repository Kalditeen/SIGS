# Architecture Audit

This document describes the current architecture after Phase 0 cleanup and defines the boundary between retained Stage2 code and the new SFG network-structure generator.

## Current Data Flow

```text
PDE-specific spec (equations.py, PDESpec)
        |
        v
SIGS activation sampling (FlexibleVectorSampler)
        |
        v
Fixed code vocabulary + widths + lift_to_nnsca(ch_common)
        |
        v
Parameterized SymPy expression
        |
        v
pde_common Stage2:
  residual -> coefficient extraction -> branch solving
  -> raw PDE residual verification -> branch classification
```

The old flow works for the historical BBM/CH/KdV experiments, but it is locked to fixed activation codes and a fixed layer-wise template. The new architecture must replace the top half while keeping the bottom half.

## Retained Modules

### Core Stage2 and PDE support

- `scripts/pdes/pde_common.py`: existing Stage2 symbolic solve and raw residual verification.
- `scripts/pdes/equations.py`: `PDESpec` instances for Gardner/BBM/CH/KdV.
- `scripts/pdes/maple_export.py`: human-runnable Maple export/import support.
- `scripts/ch/ch_common.py`: support code for the existing engine.
- `src/sigs/jacobi.py`: Jacobi elliptic functions, derivatives, and numeric backends.

### SFG modules introduced in Gardner Phase 2-4

- `sfg_bbm_21.py`: shared candidate, trial, solver, and verification path.
- `sfg_gardner.py`: Gardner residual and Gardner-specific report helpers.
- `sfg_reduction.py`: Jacobi and sech identity reduction.
- `sfg_families.py`: elementary, hyperbolic, Jacobi, and mixed streams.
- `sfg_graph.py`: first layered network graph.
- `sfg_dag.py`: lazy DAG with node derivative caching.

## Modules That Must Change

### Replace fixed `codes + widths`

The old entry path through `pde_common._nnsca_role_candidates`, `ch_common.lift_to_nnsca`, and fixed `widths` must be downgraded to a compatibility adapter. The main flow must accept a complete `AnsatzCandidate` network structure.

### New SFG network generator

The new SFG must generate full network candidates:

- per-node unique activation;
- per-node upstream connections;
- per-connection weights;
- per-node biases;
- output weights and output bias;
- configurable depth, width, and connection bounds.

### New AnsatzCompiler

A dedicated compiler must translate `AnsatzCandidate` into a parameterized SymPy expression plus:

- unknown parameter list;
- parameter role registry;
- activation function map;
- network topology description;
- stable candidate identifier;
- compile log.

The compiler must support mixed partial derivatives, not just `u_x`, `u_t`, `u_xxx`.

## Stage2 Protection Rule

Stage2 remains responsible for:

- residual construction from a supplied parameterized expression;
- coefficient extraction;
- algebraic branch solving;
- raw PDE residual identity verification;
- branch classification.

Stage2 should not be rewritten in this phase. If its interface blocks the new data flow, the first option is a small adapter. No solver result may be labeled exact without raw residual identity verification.

## New/Old Interface Relationship

```text
New:
PDE input
  -> SFG network search
  -> AnsatzCandidate
  -> AnsatzCompiler
  -> parameterized SymPy expression
  -> Stage2 adapter
  -> constraint solve + raw verification

Old:
PDE input
  -> SIGS activation sampler
  -> fixed codes/widths
  -> lift_to_nnsca
  -> pde_common Stage2
```

The old path may remain for regression tests during transition but must not be the core of new experiments.

## Immediate Risk Notes

- `pde_common.py` and `maple_export.py` still import `ch_common.py`; this is preserved.
- The full test suite still has the environment-level `pyarrow`/NumPy collection error in `tests/test_hf_data.py`.
- No existing `results/` data is migrated into the new architecture.
