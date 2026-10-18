#!/usr/bin/env python3
# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Skillware-Bench Free Model Verification Harness.

Evaluates free models on OpenRouter (e.g. nvidia/nemotron-3.5-super-vl:free)
across Vanilla Mode and Skillware-Equipped Mode on all 7 crucibles and 10 pillars.
"""

import argparse
import os
import sys
from dotenv import load_dotenv

# Ensure skillware_bench is on path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from skillware_bench.core.openrouter_engine import OpenRouterBenchmarkEngine  # noqa: E402

DEFAULT_FREE_MODELS = [
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "nvidia/nemotron-3.5-super-vl:free",
]


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Run Skillware-Bench Free Model Verification Suite via OpenRouter."
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=DEFAULT_FREE_MODELS,
        help="Free model slugs to evaluate on OpenRouter.",
    )
    parser.add_argument(
        "--crucibles",
        nargs="+",
        default=None,
        help="Optional crucible names to run (default: all 7 crucibles).",
    )
    parser.add_argument(
        "--output-dir",
        default="./runs/openrouter_sweeps",
        help="Directory to save timestamped JSON and Markdown audit reports.",
    )
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API") or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OpenRouter API key not found in OPENROUTER_API or OPENROUTER_API_KEY.", file=sys.stderr)
        sys.exit(1)

    print(f"Starting Free Model Benchmark Sweep across {len(args.models)} model(s)...")
    engine = OpenRouterBenchmarkEngine()
    _ = engine.run_sweep(
        models=args.models,
        crucible_filter=args.crucibles,
        sweep_name="free_model_verification",
        output_dir=args.output_dir,
    )
    print("\n[SUCCESS] Free model verification sweep completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
