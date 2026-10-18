#!/usr/bin/env python3
# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Skillware-Bench Production Paid Model Sweep Harness.

Evaluates frontier and sovereign paid models on OpenRouter across Vanilla Mode
and Skillware-Equipped Mode on all 7 crucibles and 10 pillars.
Protected by safety confirmation gates to prevent unauthorized spend.
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

# Full paid model roster requested by the user
PRODUCTION_PAID_MODELS = [
    "deepseek/deepseek-v4.1-flash-1017",
    "deepseek/deepseek-v4-pro",
    "google/gemini-4-argon",
    "google/gemini-4-argon:batch",
    "anthropic/claude-haiku-5.5",
    "mistralai/mistral-large-4-0",
    "openai/gpt-6-luna-pro:batch",
    "z-ai/glm-5.3-flashx",
    "qwen/qwen3.8-omni-flash",
    "qwen/qwen3.5-27b",
    "meta-llama/llama-4-maverick",
    "meta-llama/llama-3.3-70b-instruct",
    "inception/mercury-2.5",
    "moondream/moondream3-preview",
]


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Run Skillware-Bench Production Sweep on OpenRouter Paid Models."
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=PRODUCTION_PAID_MODELS,
        help="Paid model slugs to evaluate on OpenRouter.",
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
    parser.add_argument(
        "--confirm-paid-execution",
        action="store_true",
        help="MANDATORY SAFETY FLAG: Explicit confirmation to spend API credits on paid models.",
    )
    args = parser.parse_args()

    # Safety Gate: Prevent execution without explicit confirmation flag
    if not args.confirm_paid_execution:
        print(
            "\n[SAFETY HALT] Paid model benchmark requires explicit operator authorization!\n"
            "To execute with real paid credits, pass the flag: --confirm-paid-execution\n"
            f"Configured models ({len(args.models)}): {', '.join(args.models)}\n",
            file=sys.stderr,
        )
        sys.exit(2)

    api_key = os.environ.get("OPENROUTER_API") or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OpenRouter API key not found in OPENROUTER_API or OPENROUTER_API_KEY.", file=sys.stderr)
        sys.exit(1)

    print(f"Starting Production Paid Sweep across {len(args.models)} model(s)...")
    engine = OpenRouterBenchmarkEngine()
    _ = engine.run_sweep(
        models=args.models,
        crucible_filter=args.crucibles,
        sweep_name="production_paid_sweep",
        output_dir=args.output_dir,
    )
    print("\n[SUCCESS] Production paid benchmark sweep completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
