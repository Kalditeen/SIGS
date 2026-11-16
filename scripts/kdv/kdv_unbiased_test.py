#!/usr/bin/env python3
"""Unbiased KdV test: remove the reference-solution biases before Stage I.

The production code has two implicit biases:

1. ``_known_theta_candidates`` injects ``2*sech(x - 4t)^2`` and its
   left-moving twin directly into every seed's candidate pool.
2. ``_score_kdv_candidate`` scores candidates with an initial-condition term
   ``ic_weight * ic_mse``, where ``ic_mse`` compares each ansatz at ``t=0``
   against the reference soliton's initial profile.

This script removes only those two biases and otherwise reuses the exact same
Stage I screening. Stage II symbolic back-substitution is skipped; the script
only prints the candidate structures for manual verification. Pass ``--stage2``
to ``kdv_common.main`` if symbolic solving is ever needed again.
"""

import kdv_common as kc


def _no_known_theta(seed_code):
    """Replace the injected known travelling-wave candidates with none."""
    return iter(())


_original_score = kc._score_kdv_candidate


def _unbiased_score(expr_str, symbols, meshes, u0_fn, ic_weight=1.0):
    """Same loss as production, but with the IC-reference term forced to zero."""
    return _original_score(expr_str, symbols, meshes, u0_fn, ic_weight=0.0)


kc._known_theta_candidates = _no_known_theta
kc._score_kdv_candidate = _unbiased_score


if __name__ == "__main__":
    kc.main(widths=[2, 1])
