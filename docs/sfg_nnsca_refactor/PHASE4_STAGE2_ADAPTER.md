# Phase 4: Stage2 Adapter

## Scope

Added `src/nnsca/adapter.py` with `Stage2Adapter`.

## Behaviour

- Receives a compiled expression and residual callable.
- Reuses the existing Stage2 helpers in `scripts/pdes/sfg_bbm_21.py`:
  - raw residual construction
  - coefficient extraction
  - equation solving
  - raw residual identity verification
- Reports `symbolic_status`, `constraint_status`, `solve_status`,
  `nontrivial_status`, `substitution_status`, and
  `identity_verification_status` separately.
- Does not treat `sp.solve` success as exactness.

## Preserved code

Existing BBM and Gardner focused suites still pass after the adapter was
added.

## Status

Implemented and covered by focused tests.
