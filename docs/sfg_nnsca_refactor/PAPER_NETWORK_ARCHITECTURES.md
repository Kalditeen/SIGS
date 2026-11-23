# Paper Network Architectures

This document reconstructs the five NNSCA computation graphs required for the
revised Phase 1 regression suite.  The diagrams follow the task brief and the
programmatic builders in `src/sfg/paper_templates.py`.  Where the original
paper uses a sparse or asymmetric wiring pattern, that pattern is preserved
below rather than flattened into a fully-connected layer description.

All phase nodes have the form

\[
\xi_i=a_i x+b_i t+d_i.
\]

All compute nodes have the form

\[
z_v=b_v+\sum_{e\in \operatorname{In}(v)} w_e y_{\operatorname{src}(e)},\qquad
y_v=F_v(z_v).
\]

Output nodes are linear:

\[
u=c_0+\sum_j c_j y_j.
\]

## Framework (2-3-1)-1

Phases: `p1`, `p2`, `p3`.

Compute nodes:

- `h1 = p1`
- `h2 = p2^2`
- `h3 = cosh(p3)`

Output:

\[
u=c_0+c_{h1} h_1+c_{h2} h_2+c_{h3} h_3.
\]

## Framework (2-2-3-1)-1

Phases: `p1`, `p2`.

Compute nodes:

- `g1 = tanh(w_{p1__g1} p1 + w_{p2__g1} p2 + bias_g1)`
- `g2 = sech(w_{p1__g2} p1 + w_{p2__g2} p2 + bias_g2)`
- `h1 = g1^2`
- `h2 = exp(w_{g1__h2} g1 + w_{g2__h2} g2 + bias_h2)`
- `h3 = cn(w_{g2__h3} g2 + bias_h3, m_{h3})`

Output:

\[
u=c_0+c_{h1} h_1+c_{h2} h_2+c_{h3} h_3.
\]

## Framework (2-3-2-1)-3

Phases: `p1`, `p2`, `p3`.

Compute nodes:

- `g1 = p1`
- `g2 = p2^2`
- `g3 = cosh(p3)`
- `h1 = exp(w_{g1__h1} g1 + w_{g2__h1} g2 + bias_h1)`
- `h2 = cn(w_{g2__h2} g2 + w_{g3__h2} g3 + bias_h2, m_{h2})`

Output:

\[
u=c_0+c_{h1} h_1+c_{h2} h_2.
\]

## Framework (2-2-2-1)-2

Phases: `p1`, `p2`.

Compute nodes:

- `g1 = sn(w_{p1__g1} p1 + w_{p2__g1} p2 + bias_g1, m_{g1})`
- `g2 = cn(w_{p1__g2} p1 + w_{p2__g2} p2 + bias_g2, m_{g2})`
- `h1 = dn(w_{g1__h1} g1 + bias_h1, m_{h1})`
- `h2 = (w_{g1__h2} g1 + w_{g2__h2} g2 + bias_h2)^2`

Output:

\[
u=c_0+c_{h1} h_1+c_{h2} h_2.
\]

## Framework (2-3-2-1-1)-1

Phases: `p1`, `p2`, `p3`.

Compute nodes:

- `g1 = p1`
- `g2 = p2^2`
- `g3 = cosh(p3)`
- `h1 = exp(w_{g1__h1} g1 + w_{g2__h1} g2 + bias_h1)`
- `h2 = cn(w_{g2__h2} g2 + w_{g3__h2} g3 + bias_h2, m_{h2})`
- `k1 = tanh(w_{h1__k1} h1 + w_{h2__k1} h2 + bias_k1)`

Output:

\[
u=c_0+c_{k1} k_1.
\]

## Mapping to code

Builders live in `src/sfg/paper_templates.py`.  The IR is in
`src/sfg/network_ir.py`.  The compiler accepts this IR directly, so the same
five objects are both documentation and executable regression tests.
