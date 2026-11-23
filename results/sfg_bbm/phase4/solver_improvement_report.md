# Solver improvement report

## Added in this phase

- residual normalization tries expand, factor_terms, together, cancel.
- linear subsystem pre-solve via linsolve before nonlinear solve.
- function identity status marks supported differential identities.
- [2,2,1] branch classification detects constant, degenerate and
  equivalent-node branches.

## Main bottleneck

Most solve-success candidates still reduce to one active node. The
nonlinear solver returns low-dimensional branches, and raw BBM
verification is the final gate. For [2,2,1], expression growth is
small for these three functions, so extraction is fast.

## Next priority

1. Add a two-node-targeted nonlinear solve that penalizes or records
   branches with both output weights zero before generic solve.
2. Use differential-identity substitution to reduce sech^2/tan^2
   systems instead of polynomial coefficient extraction.
3. Keep linear subsystem pre-solve and add time measurements for each
   solver path.
