# Gardner phase-1 report

## Questions and results

1. Can the existing SFG+NNSCA architecture be transferred directly to Gardner?
   Yes for candidate generation, network construction, coefficient extraction,
   and raw-residual certification. The PDE residual and audit/report helpers
   were the only Gardner-specific pieces.

2. Which modules are fully reusable?
   SFG generation, `build_trial`, Jacobi support, `_extract_coefficient_equations`,
   `_solve_equations`, `_residual_is_zero`, and the record/status machinery.

3. Which modules needed modification and why?
   A new `sfg_gardner.py` supplies the Gardner residual and independent audit
   helpers. `sfg_bbm_21.py` only gained a sech-power reduction for certification.

4. Can the program automatically recover the Gardner benchmark?
   The raw-residual audit recovers and certifies the JacobiCN family. The
   generic unconstrained solver timed out on that particular Jacobi coefficient
   system, so automatic recovery through `sp.solve` is not yet demonstrated.

5. Which function/network combinations perform best?
   In the small probe, no [2,2,1] branch was verified. The single-node JacobiCN
   benchmark is the clearest exact family. Deeper widths currently hit the
   12-unknown solver guard.

6. Was a strictly verified new solution found?
   No. No `EXACT_VERIFIED` branch beyond the independently supplied benchmarks
   was produced in these small first-round experiments.

7. What are the current solver limitations?
   `sp.solve` is the main bottleneck for Jacobi elliptic coefficient systems;
   deeper networks exceed the 12-unknown guard; and the raw-residual checker
   needs explicit function identities for odd sech powers.

8. Does this support migration to other shallow-water equations?
   Partially. The architecture is equation-agnostic and Gardner residuals are
   handled correctly, but the constraint solver needs targeted differential
   algebra work before broader migration is credible.

## Counts from this run

- verified benchmark families: 3
- verified branches from search probes: 0
- solve-success records: 34

All counts refer to the raw-residual symbolic gate, not to `sp.solve` alone.
