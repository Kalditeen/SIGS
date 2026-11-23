#!/usr/bin/env python3
"""Sharma-Tasso-Olver validation with the NNSCA [3,2] structure."""

import pde_common
import equations

if __name__ == "__main__":
    pde_common.main(equations.STO, widths=[3, 2])
