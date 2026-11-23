# Gardner known-solution benchmarks

## Main experiment: alpha=beta=gamma=1

| id | source | trial | status |
|---|---|---|---|
| gardner_jacobi_cn | JacobiCN(z,m) | c1*JacobiCN(-c1**2*k*t/3 + k**3*t + k*t/4 + k*x, c1**2/(6*k**2)) - 1/2 | EXACT_VERIFIED |

### JacobiCN family

u = -1/2 + c1*cn(k*(x - c*t) | m),
m = c1**2/(6*k**2),
c = (4*c1**2 - 12*k**2 - 3)/12.

The raw Gardner residual for this family is certified identically zero by
SymPy.  This is the primary recovery target for the fixed coefficient
set alpha=beta=gamma=1.

## Auxiliary limits (not part of the main coefficient set)

| id | coefficients | expression | trial | status |
|---|---|---|---|---|
| kdv_limit_sech2 | 6,0,1 | sech(z)**2 | 2*k**2*sech(4*k**3*t - k*x)**2 | EXACT_VERIFIED |
| mkdv_limit_sech | 0,6,1 | sech(z) | k*sech(k**3*t - k*x) | EXACT_VERIFIED |

## Verification policy

Every benchmark above was rebuilt and substituted into the raw PDE
residual.  ``EXACT_VERIFIED`` means the raw residual was certified
identically zero by ``_residual_is_zero``; no numerical sampling and no
travelling-wave ODE was accepted as proof.
