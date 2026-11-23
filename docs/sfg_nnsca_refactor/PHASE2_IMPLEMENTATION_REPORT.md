# Phase 2 Implementation Report

## Scope

Phase 2 implements the SFG architecture-generation pipeline that turns bounded
random generation, paper-template derivation, and structural mutation into
valid, deduplicated, compiled `NetworkIR` candidates.  It does not run Stage2
and does not claim any exact PDE solution.

## Added Modules

- `src/sfg/architecture_utils.py`
  - DAG depth inference, layer grouping, reachability, deep copy, metadata
    layer tagging.
- `src/sfg/architecture_generator.py`
  - `GeneratorConfig` centralizes search-space bounds.
  - `ArchitectureGenerator` generates deterministic layered IRs and derives
    candidates from paper templates.
- `src/sfg/architecture_mutation.py`
  - `MutationConfig`, `MutationOutcome`, and `ArchitectureMutator`.
  - Operators: activation, add/remove node, add/remove/rewire edge, add/remove
    layer, and change-node-layer.
- `src/sfg/architecture_normalizer.py`
  - Canonical ID assignment by DAG depth.
  - Structural signature and equivalence checks.
  - Unreachable-node reporting without destructive pruning.
- `src/sfg/candidate_manager.py`
  - Candidate ID ownership, structural deduplication, compilation, JSON save
    and restore, parent-child lineage, and experiment statistics.
- `scripts/run_architecture_generation.py`
  - Deterministic experiments A-E.

## Key Decisions

- Node-scoped activations are preserved everywhere.  No candidate is converted
  back to legacy `codes + widths`.
- Layer information is inferred from the DAG rather than stored as a second
  source of truth.
- Canonicalisation is intentionally structural only.  Mathematical-expression
  equivalence and parameter-solution equivalence are kept as separate future
  concerns.
- Duplicate candidates are retained in the manager with status `DUPLICATE` so
  deletion is auditable instead of silent.
- Invalid mutation outcomes are never registered; the mutator returns
  `valid=False` and the manager's `register` validates again before storing.

## Experiment Results

Command:

```bash
PYTHONPATH=src python3 scripts/run_architecture_generation.py \
  --seed 2026 --num-candidates 12
```

Observed summary:

- generated candidates: 68
- unique candidates: 56
- duplicate candidates: 12
- invalid candidates: 0
- distinct depths: 4
- distinct node counts: 8
- compiler success: 56
- compiler failure: 0
- reproducible generation: true

Raw JSON is written to
`results/phase2_architecture_generation/candidates.json`, `stats.json`, and
`run_config.json`.

## Acceptance Status

`SFG_ARCHITECTURE_GENERATION_MILESTONE_PASSED`

All Phase 2 acceptance criteria are implemented and covered by the new test
suite; historical Phase 1 tests remain passing in the broad regression run.
