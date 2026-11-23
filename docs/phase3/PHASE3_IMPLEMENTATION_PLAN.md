# Phase 3-A Implementation Plan

## 1. Verified Interfaces

`CandidateManager.load(path)` returns a `CandidateManager` whose `records` list
contains `CandidateRecord` objects.  Each `CandidateRecord.network_ir` is a
`NetworkIR` and `compile_status` is a string.

`AnsatzCompiler.compile_ir(ir)` returns `CompiledAnsatz`.  Verified fields:

- `candidate: AnsatzCandidate`
- `expression: sympy.Expr`
- `derivative_cache: dict`
- `derivative(*orders)` and `partial(symbol, order)` methods

The candidate returned by `compile_ir` has `unknown_parameters` and
`parameter_roles` populated from `NetworkIR.parameter_symbols()` and
`NetworkIR.parameter_roles()`.

`Stage2Adapter.process(expression, residual_fn, config, pde_equation=...)`
returns a dictionary with the keys documented in the audit: `symbolic_status`,
`constraint_status`, `extraction_status`, `solve_status`,
`verification_status`, `exact_solutions`, `solutions`, `branch_attempts`,
`nontrivial_status`, `substitution_status`, `identity_verification_status`,
`failure_reason`, and `timing`.  It does not currently accept a `Stage2Input`.

The Stage2 helpers live in `scripts/pdes/sfg_bbm_21.py`:

- `_extract_coefficient_equations(residual, x, t)` -> `(equations, basis, error)`
- `_solve_equations(equations, unknowns, timeout)` -> `(raw_result, error)`
- `_residual_is_zero(expr)` -> `bool`
- `_call_with_timeout(fn, seconds)` -> `(result, error)`

`analyze_effective_network(ir, constraints, compiler=None)` returns
`EffectiveNetworkResult` and does not mutate the IR.

Gardner residual should be imported as `src.pdes.gardner.gardner_residual`.
The old `scripts/pdes/sfg_gardner.gardner_residual` is equivalent but should
not be copied again.

## 2. Implementation Shape

New package:

```text
src/nnsca/search/
    __init__.py
    automatic_solver.py
```

`AutomaticSolver` will own orchestration only.  It will:

1. Select `CandidateRecord` objects from a `CandidateManager`.
2. Recompile `record.network_ir` with `AnsatzCompiler.compile_ir`.
3. Build a parameter-consistency record from IR symbols/roles and compiled
   expression symbols.
4. Run `Stage2Adapter.process(expression, gardner_residual, solver_config)`.
5. Map raw Stage2 statuses to the Phase 3-A status vocabulary.
6. For every verified branch, call `analyze_effective_network` with the branch
   constraints.
7. Return serialisable result dictionaries and support batch save.

## 3. Parameter Consistency

The solver keeps Stage2's existing `free_symbols` extraction, but also reads:

- `record.network_ir.parameter_symbols()`
- `record.network_ir.parameter_roles()`

It computes:

- `expression_unknowns`: symbols in `expression.free_symbols - {x,t}`
- `ir_parameters`: symbols from `parameter_symbols()`
- `unused_ir_parameters`: in IR but not expression
- `missing_from_ir`: in expression but not IR
- `special_parameters`: IR symbols in the `special_function_parameter` role
- `consistent`: true when `missing_from_ir` is empty

Unused IR parameters are recorded but are not added to the Stage2 system.
Missing expression symbols indicate a symbol-identity or compiler problem and
are recorded as a warning, not silently added.

## 4. Status Mapping

Raw Stage2 result is retained in full under `stage2_record`.  The automatic
solver adds a coarse status:

- `COMPILE_FAILED`
- `COMPILED`
- `RESIDUAL_FAILED`
- `CONSTRAINT_FAILED`
- `SOLVER_TIMEOUT`
- `NO_SOLUTION`
- `SOLUTION_FOUND`
- `VERIFICATION_FAILED`
- `EXACT_VERIFIED`

Mapping rules:

- compile exception -> `COMPILE_FAILED`
- residual Stage2 error/timeout before extraction -> `RESIDUAL_FAILED`
- extraction error/timeout -> `CONSTRAINT_FAILED`
- solve timeout -> `SOLVER_TIMEOUT`
- no solutions -> `NO_SOLUTION`
- solve success and any branch verified -> `EXACT_VERIFIED`
- solve success but no branch verified -> `VERIFICATION_FAILED`
- other unresolved -> `CONSTRAINT_FAILED`

Degeneracy is recorded separately as `DEGENERATE`, `NONDEGENERATE`, or
`UNKNOWN`.

## 5. Timeout and Exception Isolation

`Stage2Adapter.process` already uses `sfg._call_with_timeout`, which uses
`SIGALRM` in the main thread.  The automatic solver will therefore run in the
main process/thread and wrap each candidate in a broad `try/except`.  It will
not create worker threads pretending to cancel blocked SymPy work.  If a
process-level isolation path is later required, it will be implemented as a
separate process, not a thread timeout.

## 6. Effective Network Analysis

For each verified branch, the solver constructs a symbol-keyed constraint dict
and calls:

```python
analyze_effective_network(
    record.network_ir,
    constraints,
    compiler=AnsatzCompiler(),
)
```

The returned classification is attached to the branch and to the candidate
result.  `EXACT_NONDEGENERATE_MULTI_NODE` maps to `NONDEGENERATE`; other
non-trivial classifications map to `DEGENERATE`; exceptions map to `UNKNOWN`.

## 7. Experiment Script

New script: `scripts/run_phase3_automatic_solving.py`.

It will:

- load `results/phase2_architecture_generation/candidates.json`;
- accept candidate IDs, count, timeouts, max expression nodes, seed;
- select representative candidates from actual IR data;
- run `AutomaticSolver`;
- save a unique run directory under `results/phase3_automatic_solving/`.

Representative categories:

- Jacobi-containing candidate
- two-node candidate
- two-node heterogeneous candidate
- two-layer candidate

If a category is absent, the run report records that fact.  No candidate is
handcrafted to fill the category.

## 8. Test Plan

New tests in `tests/test_phase3_automatic_solver.py` cover:

- single candidate run
- batch continuation after one candidate failure
- compile failure
- constraint extraction failure
- solver timeout
- solution-found but verification-failed
- exact-verified branch
- parameter-role consistency
- effective-network analysis
- multi-candidate batch

The solver will accept an injectable Stage2 adapter in tests.  Real integration
is exercised by `scripts/run_phase3_automatic_solving.py`, which uses the real
`Stage2Adapter`.

## 9. Regression Plan

After implementation:

- run new `tests/test_phase3_automatic_solver.py`
- run Phase 2 architecture tests
- run Phase 1 paper/compiler tests
- run broad suite excluding `tests/test_hf_data.py`
- record the known `pyarrow` issue separately

## 10. Delivery

- `src/nnsca/search/automatic_solver.py`
- `scripts/run_phase3_automatic_solving.py`
- `tests/test_phase3_automatic_solver.py`
- `docs/phase3/PHASE3_A_INTEGRATION_REPORT.md`
- run outputs under `results/phase3_automatic_solving/run_*/`

Completion flag: `PHASE3_A_INTEGRATION_COMPLETED`
