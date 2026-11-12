#!/usr/bin/env python3
"""Camassa-Holm validation with the NNSCA [2,3,2,1,1] structure."""

import ch_common

if __name__ == "__main__":
    ch_common.main_full_expressions(widths=[3, 2, 1])
