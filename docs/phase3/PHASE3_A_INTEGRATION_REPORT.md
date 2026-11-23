# Phase 3-A Integration Report

## Result

`PHASE3_A_INTEGRATION_COMPLETED`

The IR-aware automatic solving layer is implemented and has completed a real
run against the existing Gardner Stage2 path.  The run did not find a verified
exact solution, and the failure stages are recorded below rather than
misreported as success.

## 1. Did NetworkIR Enter Stage2?

Yes.  Each `CandidateRecord.network_ir` was recompiled with
`AnsatzCompiler.compile_ir`, and the resulting SymPy trial was passed to the
real `Stage2Adapter` using `src/pdes/gardner.gardner_residual`.

Representative run:

```text
selected candidates: candidate_0002, candidate_0046
missing category: jacobi_single_node
```

- `candidate_0002` is the paper `(2-2-3-1)` template, containing JacobiCN and
  a two-layer structure.
- `candidate_0046` is a two-node heterogeneous candidate with `sech` and
  `tanh`.

## 2. Was the Existing Jacobi Benchmark Recovered?

No.  The Phase 2 candidate pool contains no single-node Jacobi candidate, so
the run records `jacobi_single_node` as missing rather than handcrafting one.
No exact Jacobi branch was recovered from the selected representatives.

This is an integration result, not a claim that the benchmark is impossible.

## 3. Which Candidates Completed the Full Solve Path?

Neither representative candidate reached a verified solution:

- `candidate_0002`: `CONSTRAINT_FAILED`
- `candidate_0046`: `CONSTRAINT_FAILED`

Both still completed the orchestration path and produced persisted results;
their raw Stage2 records are retained.

## 4. Where Did Candidates Fail?

- `candidate_0002`
  - `constraint_status`: `timeout`
  - `extraction_status`: `timeout`
  - `verification_status`: `SYMBOLIC_UNRESOLVED`
  - reason: `coefficient extraction timeout`
- `candidate_0046`
  - `constraint_status`: `success`
  - `extraction_status`: `success`
  - `solve_status`: `unsupported`
  - `verification_status`: `SYMBOLIC_UNRESOLVED`
  - reason: `coefficient solve system too large`

## 5. Were There Timeouts?

Yes, one timeout was observed in constraint extraction for `candidate_0002`.
`candidate_0046` did not time out; it hit the existing unknown/equation size
guard in the Stage2 solver.

## 6. Was Network Degeneracy Observed?

No verified exact branches existed, so effective-network analysis was not
meaningful for these candidates.  Degeneracy is therefore recorded as
`UNKNOWN`.  The analysis function is wired into the exact-branch path and is
covered by unit tests.

## 7. Were Parameter Roles Preserved?

Yes.  The automatic solver records both the Stage2-derived expression
unknowns and the IR-derived parameter list and roles.  The consistency check
was run before Stage2 and is stored for each candidate.

## 8. Main Current Bottleneck

The main bottleneck is the existing symbolic constraint extraction/solver on
multi-node and nested activations:

1. Paper-template nested networks can exceed the coefficient-extraction time
   budget.
2. Even when extraction succeeds, the resulting algebraic system can exceed
   the existing equation/unknown guard.

The next step should be Phase 3-B or a bounded solver diagnostic.  No Stage2
core was rewritten during this phase.

## Test Results

- New Phase 3-A solver tests: `11 passed`
- Broad regression excluding known HF-data environment issue: `168 passed`
- Full-suite collection still fails only at `tests/test_hf_data.py` with
  `pyarrow requires NumPy 2.0 or newer, found 1.26.4`.

## Outputs

- Implementation plan: [PHASE3_IMPLEMENTATION_PLAN.md](/Users/kang/SIGS/docs/phase3/PHASE3_IMPLEMENTATION_PLAN.md)
- Solver: [automatic_solver.py](/Users/kang/SIGS/src/nnsca/search/automatic_solver.py)
- Script: [run_phase3_automatic_solving.py](/Users/kang/SIGS/scripts/run_phase3_automatic_solving.py)
- Tests: [test_phase3_automatic_solver.py](/Users/kang/SIGS/tests/test_phase3_automatic_solver.py)
- Run results: [results/phase3_automatic_solving](/Users/kang/SIGS/results/phase3_automatic_solving)
