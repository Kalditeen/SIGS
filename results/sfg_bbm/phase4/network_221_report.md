# [2,2,1] network report

## Experiment B summary

| expression | status | solve | exact branches | branch kind |
|---|---|---|---|---|
| sech(z)**2 | EXACT_VERIFIED | success | 2 | SINGLE_NODE_REDUCTION |
| tan(z)**2 | EXACT_VERIFIED | success | 2 | SINGLE_NODE_REDUCTION |
| JacobiCN(z,m)**2 | EXACT_VERIFIED | success | 2 | SINGLE_NODE_REDUCTION |
| sech(z)**2|tan(z)**2 | EXACT_VERIFIED | success | 2 | SINGLE_NODE_REDUCTION |
| JacobiCN(z,m)**2|sech(z)**2 | EXACT_VERIFIED | success | 2 | SINGLE_NODE_REDUCTION |
| JacobiCN(z,m)**2|tan(z)**2 | EXACT_VERIFIED | success | 2 | SINGLE_NODE_REDUCTION |

## Question 1: can [2,2,1] express solutions [2,1] cannot?
The tested exact branches are single-node reductions, so this small
experiment did not find a genuinely new two-node solution family.
The network can express it, but the symbolic solver reduced one output
weight to zero in every verified branch.

## Question 2: can two independent nodes form a non-single-wave BBM solution?
Not observed in this run. Every exact branch had either w_out_0=0 or
w_out_1=0. This does not prove impossibility; it shows the current
coefficient solver prefers one-node branches.
