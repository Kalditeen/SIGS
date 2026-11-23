# Phase-5 non-degenerate two-node search report

## Result summary

| expression | verification | solve | active solve | classification |
|---|---|---|---|---|
| sech(z)**2 | EXACT_VERIFIED | success | no_solution | EXACT_SINGLE_NODE_DEGENERATE |
| tan(z)**2 | EXACT_VERIFIED | success | no_solution | EXACT_SINGLE_NODE_DEGENERATE |
| JacobiCN(z,m)**2 | EXACT_VERIFIED | success | no_solution | EXACT_SINGLE_NODE_DEGENERATE |
| sech(z)**2|tan(z)**2 | EXACT_VERIFIED | success | no_solution | EXACT_SINGLE_NODE_DEGENERATE |
| JacobiCN(z,m)**2|sech(z)**2 | EXACT_VERIFIED | success | no_solution | EXACT_SINGLE_NODE_DEGENERATE |
| JacobiCN(z,m)**2|tan(z)**2 | EXACT_VERIFIED | success | no_solution | EXACT_SINGLE_NODE_DEGENERATE |
| JacobiDN(z, m) + sech(z)**2 | FAILED | success | no_solution | IDENTITY_UNVERIFIED |
| tanh(csch(z)) | FAILED | success | no_solution | IDENTITY_UNVERIFIED |
| z**2 + tanh(alpha*z) | FAILED | success | no_solution | IDENTITY_UNVERIFIED |
| cos(z)*tanh(z) | FAILED | success | no_solution | IDENTITY_UNVERIFIED |
| JacobiDN(z, m) + sech(z)**2|tanh(csch(z)) | FAILED | success | no_solution | IDENTITY_UNVERIFIED |
| JacobiDN(z, m) + sech(z)**2|z**2 + tanh(alpha*z) | FAILED | success | no_solution | IDENTITY_UNVERIFIED |

## Question 1: was a genuinely non-degenerate two-node BBM solution found?

No verified branch in these probes had both output weights nonzero and
D = a1*b2 - a2*b1 nonzero. Every exact branch was a single-node
reduction. This is a solver result for the tested candidates, not a
proof that no such solution exists.

## Question 2: active non-degenerate solve

The auxiliary equation q*w_out_0*w_out_1*D - 1 = 0 was applied to
polynomial coefficient systems. Where the system was polynomial,
the active constraint system had no branch, or Groebner/direct solve
did not return a verified solution. Details are in
``branch_classification_report.md`` and ``solver_limitations.md``.

## Question 3: cross terms

Cross-term extraction is recorded per candidate in ``cross_term_analysis.md``.
For the same-function pairs, the w0*w1 product appears only through the
two independent phases; no identity collapsed the two terms in these
small probes.

## Question 4: can the current solver search non-degenerate branches?

The auxiliary-equation solve did run on all polynomial cases, so the
machinery is in place. For these candidates it returned no branch.
That means the current solver can target the non-degenerate set, but
it does not yet have a way to navigate the surrounding solution
varieties when Groebner/direct solve returns an empty set.

## Question 5: is hierarchical symbolic solving necessary?

For deeper all-to-all networks it is likely necessary to avoid
expanding the full residual as one polynomial system. For the current
[2,2,1] probes, cross terms are small enough to inspect directly, but
the main gap is mathematical, not scale: the extracted algebraic
system preferred single-node reductions.

## Generated candidates

- JacobiDN(z, m) + sech(z)**2|JacobiDN(z, m) + sech(z)**2: left=JacobiDN(z, m) + sech(z)**2 right=JacobiDN(z, m) + sech(z)**2 source=generated rule=phase5_auto_pair
- tanh(csch(z))|tanh(csch(z)): left=tanh(csch(z)) right=tanh(csch(z)) source=generated rule=phase5_auto_pair
- z**2 + tanh(alpha*z)|z**2 + tanh(alpha*z): left=z**2 + tanh(alpha*z) right=z**2 + tanh(alpha*z) source=generated rule=phase5_auto_pair
- cos(z)*tanh(z)|cos(z)*tanh(z): left=cos(z)*tanh(z) right=cos(z)*tanh(z) source=generated rule=phase5_auto_pair
- JacobiDN(z, m) + sech(z)**2|tanh(csch(z)): left=JacobiDN(z, m) + sech(z)**2 right=tanh(csch(z)) source=generated rule=phase5_auto_pair
- JacobiDN(z, m) + sech(z)**2|z**2 + tanh(alpha*z): left=JacobiDN(z, m) + sech(z)**2 right=z**2 + tanh(alpha*z) source=generated rule=phase5_auto_pair

