# Gardner residual verification

Raw residual: `u_t + 1*u*u_x + 1*u**2*u_x + 1*u_xxx`.

The cubic term is implemented as `u**2 * diff(u, x)`, not
`u * diff(u, x)**2`.  Third-order space derivatives are computed by
`sp.diff(u, X, 3)`.  No travelling-wave ODE or numerical sampling is
used as an exactness proof.

| candidate | verification | solver | identity |
|---|---|---|---|
| func_0001: JacobiDN(z, m) + sech(z)**2 | FAILED | success | skipped |
| func_0002: tanh(csch(z)) | FAILED | success | skipped |
| func_0003: z**2 + tanh(alpha*z) | FAILED | success | skipped |
| func_0004: cos(z)*tanh(z) | FAILED | success | skipped |
| func_0005: log(z) + exp(-z) | FAILED | success | skipped |
| func_0006: z**6 | FAILED | success | skipped |
| func_0007: exp(-2*z) | FAILED | success | skipped |
| func_0008: tanh(exp(-z**2)) | FAILED | success | skipped |
| func_0009: exp(-z)*cosh(z) | FAILED | success | skipped |
| func_0010: cosh(z)**2 | FAILED | success | skipped |
| func_0012: tanh(alpha*z)**2 | FAILED | success | skipped |
| func_0013: tanh(sinh(z)) | FAILED | success | skipped |
| func_0015: tanh(z) | FAILED | success | skipped |
| func_0016: exp(-z)*csch(z) | FAILED | success | skipped |
| func_0017: tan(z)*JacobiSN(z, m) | FAILED | success | skipped |
| func_0018: tan(z)**2 | FAILED | success | skipped |
| func_0019: z + log(z) | FAILED | success | skipped |
| func_0020: z**2 + cosh(z) | FAILED | success | skipped |
| func_0021: z**3 + log(z) | FAILED | success | skipped |
| func_0022: sinh(z)**2 | FAILED | success | skipped |
| func_0023: tanh(sin(z)*cosh(z)) | FAILED | success | skipped |
| func_0024: exp(2*z) | FAILED | success | skipped |
| func_0025: 2*JacobiDN(z, m) | SYMBOLIC_UNRESOLVED | timeout | skipped |
| func_0027: tanh(sech(z)**2) | FAILED | success | skipped |
| func_0028: JacobiCN(z, m)**2 | FAILED | success | skipped |
| func_0029: tanh(tanh(alpha*z)) | FAILED | success | skipped |
| func_0030: exp(z) + tanh(alpha*z) | FAILED | success | skipped |
