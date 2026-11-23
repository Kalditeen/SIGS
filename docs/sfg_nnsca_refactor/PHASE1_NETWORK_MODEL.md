# Phase 1: Network Data Model

## Scope

Added the core explicit network model under `src/nnsca/`:

- `models.py`: `NetworkNode`, `NetworkConnection`, `NetworkStructure`,
  `OutputTerm`, and `AnsatzCandidate`.
- `registry.py`: `ParameterRegistry` with role tracking.
- `src/sfg/atoms.py`: immutable `ActivationAtom` registry covering elementary,
  trigonometric, hyperbolic, and Jacobi functions, including squared forms.

## Decisions

- SFG candidates are complete network structures, not activation-code lists.
- Connections and output terms are explicit data, so sparse and future skip
  connections do not depend on a fixed `codes + widths` template.
- Jacobi functions are first-class activation atoms with their modulus-square
  parameter `m`.
- Special-function parameters are scoped per node during compilation, so two
  independent Jacobi nodes do not silently share one parameter.

## Status

Implemented and covered by `tests/test_sfg_nnsca_refactor.py`.
