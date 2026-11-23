# Phase 2: Ansatz Compiler

## Scope

Added `src/nnsca/compiler.py` with `AnsatzCompiler` and `CompiledAnsatz`.

## Behaviour

- Walks an explicit `NetworkStructure` and builds the parameterised SymPy
  expression `u_trial(x,t)`.
- Keeps independent activation functions per node.
- Supports arbitrary connection patterns because each edge is explicit.
- Supports general mixed derivatives via `CompiledAnsatz.derivative(...)`.
- Caches repeated derivatives and avoids pre-expanding every intermediate
  expression.

## PDE independence

The compiler never imports Gardner, BBM, or CH definitions.  PDE-specific
logic lives in `src/pdes/`.

## Status

Implemented and covered by focused tests.
