# Phase 6: Cross-Equation Preparation

## Scope

Added `src/pdes/` with a PDE-independent `PDESpec` contract plus Gardner, BBM,
and Camassa-Holm specifications.

## PDE definitions

- Gardner: `u_t + u*u_x + u**2*u_x + u_xxx = 0`
- BBM: `u_t + u_x + u*u_x - u_{xxt} = 0`
- Camassa-Holm: standard mixed-derivative form with `u_{xxt}` and `u_{xxx}`.

## Guarantees

The compiler computes general mixed derivatives, so BBM's `u_{xxt}` and CH's
mixed terms do not require Gardner-specific derivative logic.  No new BBM or
CH solutions were asserted in this phase; the point is that the pipeline is
not locked to Gardner.
