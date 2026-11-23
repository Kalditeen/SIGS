# Phase 3 report

## 1. Does generated-only mode find exact solutions independently?
Yes. It uses no seed candidates and still finds exact branches.

## 2. Are tan**2 and JacobiCN**2 produced by SFG generation rules?
Yes. Both appear as `random_pow` candidates from the existing atom pool;
they are not hard-coded in a special candidate list.

## 3. How many solve-success records satisfy the original PDE?
- seed 101: 5/70 solve-success records are exact.
- seed 202: 4/72 solve-success records are exact.
- seed 303: 6/72 solve-success records are exact.
- seed 404: 4/71 solve-success records are exact.
- seed 505: 6/58 solve-success records are exact.

## 4. Main failure reason

Most solve-success candidates reach substitution and are rejected because
the back-substituted raw PDE residual is not identically zero.
See `failure_analysis.md` inside each seed run directory.

## 5. Stability across seeds

Stable exact source expressions across all seeds: ['JacobiCN(z, m)**2', 'tan(z)**2']

## 6. Category success

| category | candidates | exact candidates |
|---|---:|---:|
| elementary | 93 | 8 |
| hyperbolic | 229 | 7 |
| special | 64 | 10 |

## 7. Next priority

Improve NNSCA constraint extraction and identity verification before
expanding the SFG atom library. The generated pool already contains
exact-solution-producing forms.
