# Phase 3-B Complex Network Audit

This audit selects real Phase 2 candidates for six structural
categories and runs each through the original Gardner Stage2 path.
A candidate may represent more than one category, so the table records
its full structural profile.

## Selection

| category | candidate | nodes | depth | activations |
|---|---|---|---|---|
| A | candidate_0057 | 1 | 1 | tan |
| B | candidate_0046 | 2 | 1 | sech, tanh |
| C | candidate_0002 | 5 | 2 | JacobiCN, exp, sech, square, tanh |
| D | candidate_0003 | 5 | 2 | JacobiCN, cosh, exp, identity, square |
| E | candidate_0041 | 6 | 3 | JacobiCN, cosh, exp, identity, square, tanh |
| F | candidate_0001 | 3 | 1 | cosh, identity, square |

## Results

| candidate | status | degeneracy | failure reason |
|---|---|---|---|
| candidate_0001 | CONSTRAINT_FAILED | UNKNOWN | coefficient solve system too large |
| candidate_0002 | CONSTRAINT_FAILED | UNKNOWN | coefficient solve system too large |
| candidate_0003 | CONSTRAINT_FAILED | UNKNOWN | coefficient solve system too large |
| candidate_0041 | CONSTRAINT_FAILED | UNKNOWN | coefficient solve system too large |
| candidate_0046 | CONSTRAINT_FAILED | UNKNOWN | coefficient solve system too large |
| candidate_0057 | VERIFICATION_FAILED | UNKNOWN | solver produced branches but none passed independent back-substitution verification |

## Failure-stage distribution

- CONSTRAINT_FAILED: 5
- VERIFICATION_FAILED: 1

Only branches certified by raw Gardner residual identity are reported as
exact.  A failed solve is recorded as a failure stage, never as a proof
that no exact solution exists.

