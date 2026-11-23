# BBM [2,3,2,1] solver exploration

## What changed

The SFG script now accepts `--widths` and can build either the original
`[2,1]` affine-phase trial or a real `[2,3,2,1]` hierarchical trial:

```text
h1_j = f(w1_jx*x + w1_jt*t + b1_j)
h2_k = f(sum_j w2_kj*h1_j + b2_k)
u    = b_out + sum_k w_out_k*h2_k
```

The `[2,1]` path is unchanged and remains the default.

## What the diagnostics show

### [2,1] mixed run, 30 candidates

- symbolic success: 30/30
- constraint extraction success: 29/30
- solve success: 27/30
- exact branches: 4
- exact candidates: 3
- distinct exact solutions: 3

The important distinction is that `solve_status=success` means SymPy returned
coefficient assignments, not that the PDE was solved. Of the 27 solve-success
candidates, only 3 survive independent raw-residual verification. The other
24 returned only constant or degenerate branches:

- CONSTANT_TRIVIAL branches: 40
- DEGENERATE branches: 27
- NONTRIVIAL branches: 4

### [2,3,2,1] generated-only run, 3 candidates

- symbolic success: 3/3
- constraint extraction success: 0/3
- solve reached: 0/3
- exact: 0

All three deep-network candidates fail before the solver is called. Two fail
during coefficient extraction and one times out. The full two-hidden-layer
trial has 20 free network weights, and nesting `f` into the second layer makes
the raw BBM residual explode before a polynomial coefficient system can be
formed.

## Why some candidates work and most do not

The BBM residual for the trial has three competing types of terms:

- linear derivative terms from `u_t + u_x`
- nonlinear terms from `u*u_x`
- dispersion terms from `-u_xxt`

For `sech(z)**2`, `tan(z)**2`, and `JacobiCN(z,m)**2`, the derivative algebra
allows those three groups to cancel. In particular, squaring preserves enough
structure that `f*f_z` and `f_zzz` stay in the same function basis, so the
extracted coefficient equations admit a nontrivial `c1 != 0` branch.

For most generated candidates, the extracted equations contain incompatible
monomials such as `a*c1**2` and `-a*c1**2` together. The only symbolic
solutions are `c1=0`, or `a=b=0`, or equivalent degeneracies. SymPy still
returns those as successful coefficient solutions, and only the later
back-substitution check rejects them.

The deep `[2,3,2,1]` network does not help this bottleneck. It makes the
bottleneck occur earlier by increasing expression size before any structural
cancellation can be identified.

## Recommended solver improvements

1. Split `solve_status` from exactness permanently. Treat coefficient solve as
   an intermediate stage, exactly as the current records already do.

2. Add a cheap pre-solve filter that detects incompatible quadratic/dispersion
   monomials before calling `sp.solve`. For example, equations containing
   `a*c1**2` and `-a*c1**2` plus no compatible third-derivative term can be
   rejected without a full nonlinear solve.

3. Solve linear parameter subsystems first with `sp.linsolve`, substitute the
   result, and only call the nonlinear solver on the reduced system. This is
   the highest-value performance change for the current `[2,1]` candidates.

4. For deep networks, do not feed every generated activation through every
   layer. Use sparse or identity-initialized structural templates, or solve a
   reduced last-layer problem first. This controls expression growth before
   residual extraction.

5. Keep per-candidate stage timeouts and record failures by stage. The current
   `solver_diagnosis.md` shows that `[2,1]` is dominated by 24
   `solver_branches_not_exact` records, while `[2,3,2,1]` is dominated by
   extraction failures.

The next implementation priority should be the linear-subsystem pre-solve and
trivial-branch rejection, not expanding the SFG atom library or the network
depth.
