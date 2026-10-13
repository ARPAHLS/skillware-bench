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

from skillware_bench.core.adapters import (  # noqa: E402
    AdapterRegistry,
    BaseModelAdapter,
    ModelResponse,
    TokenUsage,
    get_adapter,
)
from skillware_bench.core.agent_loop import AgentLoop  # noqa: E402
from skillware_bench.core.evaluators import CrucibleEvaluator  # noqa: E402
from skillware_bench.core.perturbations import PerturbationEngine  # noqa: E402
from skillware_bench.core.provenance import ProvenanceEngine  # noqa: E402
from skillware_bench.core.runner import HarnessRunner  # noqa: E402
from skillware_bench.core.statistics import StatisticalEvaluator  # noqa: E402
from skillware_bench.dashboard import DashboardGenerator  # noqa: E402
from skillware_bench.suites import ALL_CRUCIBLES  # noqa: E402
from skillware_bench.viz import VisualGenerator  # noqa: E402

__version__ = "0.1.0"
__author__ = "ARPA Hellenic Logical Systems"

__all__ = [
    "__version__",
    "__author__",
    "HarnessRunner",
    "AgentLoop",
    "CrucibleEvaluator",
    "ProvenanceEngine",
    "PerturbationEngine",
    "StatisticalEvaluator",
    "DashboardGenerator",
    "VisualGenerator",
    "AdapterRegistry",
    "BaseModelAdapter",
    "ModelResponse",
    "TokenUsage",
    "get_adapter",
    "ALL_CRUCIBLES",
]
