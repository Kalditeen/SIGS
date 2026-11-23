#!/usr/bin/env python3
"""Variable-coefficient Burgers validation with the NNSCA [3,2] structure."""

import pde_common
import equations

if __name__ == "__main__":
    pde_common.main(equations.VCBURGERS, widths=[3, 2])
