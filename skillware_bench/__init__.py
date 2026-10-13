# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Skillware-Bench: The Empirical Benchmark & Evaluation Harness for Governed Agent Skills."""

import os
import sys


def _sanitize_import_paths() -> None:
    """Ensure installed packages take precedence over local reference checkout directories."""
    cwd = os.getcwd()
    for p in ["", cwd]:
        if p in sys.path:
            cand = os.path.join(p, "skillware")
            if os.path.isdir(cand) and not os.path.isfile(os.path.join(cand, "__init__.py")):
                try:
                    sys.path.remove(p)
                except ValueError:
                    pass


_sanitize_import_paths()

__version__ = "0.1.0"
__author__ = "ARPA Hellenic Logical Systems"

__all__ = ["__version__", "__author__"]
