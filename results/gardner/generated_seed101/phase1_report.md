# SFG + NNSCA Gardner search report

- coefficients: alpha=1, beta=1, gamma=1
- generated candidates: 30
- unique candidates after structural dedup: 27
- candidates with symbolic analysis success: 27
- candidates with constraint extraction success: 27
- candidates with solver success: 26
- verified exact branches: 0
- verified exact candidates: 0
- distinct exact solutions after equivalence: 0

## Seed/generated split

- seed candidates: 0
- generated candidates: 30

## Candidate quality

- category distribution: {'special': 4, 'hyperbolic': 16, 'elementary': 7}
- depth distribution: {1: 20, 2: 6, 0: 1}
- node count range: 2..8
- complexity range: 1..4

## Result classification

{'IDENTITY_UNVERIFIED': 26, 'UNSUPPORTED': 1}

## Verified branches

Only branches whose raw Gardner residual was certified identically zero
by ``_residual_is_zero`` are listed as exact.
