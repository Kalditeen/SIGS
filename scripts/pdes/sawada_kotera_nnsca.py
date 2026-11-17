#!/usr/bin/env python3
"""Sawada-Kotera validation with the NNSCA [2,1] structure."""

import pde_common
import equations

if __name__ == "__main__":
    pde_common.main(equations.SAWADA_KOTERA, widths=[2, 1])
