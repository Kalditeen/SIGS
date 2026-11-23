#!/usr/bin/env python3
"""KdV validation with the generic NNSCA PDE engine.

Known travelling-wave soliton:

    u(x, t) = (1/2) * sech((x - t) / 2)**2

for ``u_t + 6*u*u_x + u_xxx = 0``.
"""

import pde_common
import equations

if __name__ == "__main__":
    pde_common.main(equations.KDV, widths=[3])
