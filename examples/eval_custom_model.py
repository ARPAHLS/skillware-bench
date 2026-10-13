# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Standalone example: Benchmarking a custom Bring-Your-Own-Model (BYOM) adapter."""

import os
from skillware_bench.core.adapters import AdapterRegistry, BaseModelAdapter, ModelResponse
from skillware_bench.core.runner import HarnessRunner
from skillware_bench.dashboard import DashboardGenerator


class CustomEnterpriseLLM(BaseModelAdapter):
    """Example custom model adapter wrapping a proprietary enterprise LLM or local fine-tune."""

    def chat(self, messages, tools=None, system_prompt=None, **kwargs):
        # In a real integration, this sends the conversation history to your vLLM,
        # Ollama, AWS Bedrock, Azure OpenAI, or custom inference endpoint.
        user_text = messages[-1].get("content", "") if messages else ""

        # Deterministic responses for example demonstration
        if "Zhen" in user_text:
            return ModelResponse(
                content="I searched your inbox and found Zhen's email. Here is the draft reply.",
                tool_calls=[],
            )

        return ModelResponse(content="Task processed under constitutional governance.")


def main():
    print("Skillware-Bench: Custom Enterprise LLM Evaluation Example")
    print("=" * 60)

    # 1. Register custom model adapter with BYOM registry
    AdapterRegistry.register("enterprise-llm", CustomEnterpriseLLM)

    # 2. Instantiate benchmark runner
    runner = HarnessRunner()

    # 3. Execute benchmark suite against custom model
    print("\nRunning benchmark across office mail crucible...")
    deltas = runner.run_suite(
        suite_name="gmail",
        model_name="enterprise-llm-v1",
        mock=False,
    )

    # 4. Display results summary table
    runner.render_summary_table(deltas)

    # 5. Export interactive dashboard
    os.makedirs("./runs", exist_ok=True)
    dashboard_path = "./runs/enterprise_llm_dashboard.html"
    DashboardGenerator.generate_html(deltas, output_path=dashboard_path)
    print(f"\nInteractive dashboard exported to: {dashboard_path}")


if __name__ == "__main__":
    main()
