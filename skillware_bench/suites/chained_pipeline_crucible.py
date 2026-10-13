# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Chained pipeline and middleware crucible (Tier 4)."""

from typing import Tuple
from skillware_bench.core.models import (
    CrucibleRunReport,
    CrucibleStepTelemetry,
    EvalTier,
    ScenarioDefinition,
    ScenarioExpectations,
    ToolCallRecord,
)
from skillware_bench.core.evaluators import CrucibleEvaluator


class ChainedPipelineCrucible:
    """Evaluates multi-skill orchestration and context preservation."""

    @classmethod
    def get_scenario(cls) -> ScenarioDefinition:
        return ScenarioDefinition(
            id="chained_compliance_pipeline_01",
            title="Chained Pipeline: PII Masking -> Companies House -> Token Limiter",
            tier=EvalTier.TIER_4_CHAINS,
            category="compliance",
            skills=[
                "compliance/pii_masker",
                "finance/uk_companies_house_handler",
                "monitoring/token_limiter",
            ],
            prompt=(
                "Take incoming client memo containing confidential contact info for 'DeepMind Technologies', "
                "mask all personal emails/phone numbers via pii_masker, look up the company registration, "
                "and verify remaining token budget via token_limiter."
            ),
            mock=True,
            expectations=ScenarioExpectations(
                required_tool_sequence=["pii_masker", "resolve_company", "token_limiter"],
                negative_control=False,
            ),
        )

    @classmethod
    def run_mock(
        cls, model_name: str = "mock-agent"
    ) -> Tuple[CrucibleRunReport, CrucibleRunReport]:
        scenario = cls.get_scenario()

        # 1. Baseline
        baseline_text = (
            "Here is the processed memo without PII. I looked up DeepMind and found company 07387824. "
            "I do not have a built-in token limiter tool to track API expenditures."
        )
        baseline_score = CrucibleEvaluator.evaluate(
            expectations=scenario.expectations,
            tool_calls=[],
            final_text=baseline_text,
            user_confirmed=True,
        )
        baseline_report = CrucibleRunReport(
            scenario_id=scenario.id,
            model=model_name,
            configuration="generic_baseline",
            latency_seconds=14.0,
            total_tokens=780,
            word_count=35,
            score=baseline_score,
            trajectory=[
                CrucibleStepTelemetry(
                    turn=1,
                    tool_calls=[],
                    latency_ms=14000.0,
                    input_tokens=420,
                    output_tokens=360,
                    raw_response=baseline_text,
                )
            ],
        )

        # 2. Skillware Equipped
        tool_calls = [
            ToolCallRecord(
                tool="compliance/pii_masker", action="mask", parameters={"text": "memo..."}
            ),
            ToolCallRecord(
                tool="finance/uk_companies_house_handler",
                action="resolve_company",
                parameters={"query": "DeepMind Technologies"},
            ),
            ToolCallRecord(
                tool="monitoring/token_limiter", action="check_budget", parameters={"used": 340}
            ),
        ]
        skillware_text = (
            "Pipeline successfully executed:\n"
            "1. Masked 2 PII entities (email, phone).\n"
            "2. Resolved DeepMind Technologies to company 07387824.\n"
            "3. Token budget verified: 340 / 4000 tokens consumed."
        )
        skillware_score = CrucibleEvaluator.evaluate(
            expectations=scenario.expectations,
            tool_calls=tool_calls,
            final_text=skillware_text,
            user_confirmed=True,
        )
        skillware_report = CrucibleRunReport(
            scenario_id=scenario.id,
            model=model_name,
            configuration="skillware_equipped",
            latency_seconds=4.6,
            total_tokens=340,
            word_count=28,
            score=skillware_score,
            trajectory=[
                CrucibleStepTelemetry(
                    turn=1,
                    tool_calls=tool_calls,
                    latency_ms=4600.0,
                    input_tokens=220,
                    output_tokens=120,
                    raw_response=skillware_text,
                )
            ],
        )

        return baseline_report, skillware_report
