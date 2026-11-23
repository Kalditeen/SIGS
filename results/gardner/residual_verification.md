# Gardner residual verification

Raw residual implemented in `scripts/pdes/sfg_gardner.py`:

    R[u] = u_t + alpha*u*u_x + beta*u**2*u_x + gamma*u_{xxx}

The cubic nonlinearity is `u**2 * diff(u, x)` and the dispersive term
is `diff(u, x, 3)`.  No travelling-wave reduction is substituted before
verification.  For each benchmark the reconstructed `u(x,t)` is plugged
directly into this raw residual.

| id | coefficients | certified_zero | status |
|---|---|---|---|
| gardner_jacobi_cn | 1,1,1 | True | EXACT_VERIFIED |
| kdv_limit_sech2 | 6,0,1 | True | EXACT_VERIFIED |
| mkdv_limit_sech | 0,6,1 | True | EXACT_VERIFIED |

## Travelling-wave consistency

For z=x-c*t and u=U(z), substitution gives

    R = d/dz(-c*U + alpha/2*U^2 + beta/3*U^3 + gamma*U'').

This formula is used only for cross-checks and documentation; exact
solutions are still verified against the original PDE residual.
