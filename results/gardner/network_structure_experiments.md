# Gardner network-structure experiments

| widths | status | solve | failure |
|---|---|---|---|
| [2, 1] | FAILED | success | solver produced branches but none passed independent back-substitution verification |
| [2, 2, 1] | FAILED | success | solver produced branches but none passed independent back-substitution verification |
| [2, 3, 1] | SYMBOLIC_UNRESOLVED | unsupported | coefficient solve system too large |
| [2, 3, 2, 1] | SYMBOLIC_UNRESOLVED | unsupported | coefficient solve system too large |

The [2,1] and [2,2,1] runs complete the constraint solver but do not
produce a verified Gardner branch for `tanh(z)`.  The [2,3,1] and
[2,3,2,1] runs are blocked by the existing 12-unknown solver limit;
their raw residual and coefficient extraction still finish.
