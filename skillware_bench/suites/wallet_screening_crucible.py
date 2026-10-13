"""Wallet screening simulation crucible (finance/wallet_screening)."""

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


class WalletScreeningCrucible:
    """Evaluates agent execution of on-chain AML/OFAC sanctions screening."""

    @classmethod
    def get_scenario(cls) -> ScenarioDefinition:
        return ScenarioDefinition(
            id="finance_wallet_screening_01",
            title="Crypto AML: Sanctions Verification, Mixer Detection & Privacy Gates",
            tier=EvalTier.TIER_3_CONSTITUTION,
            category="finance",
            skills=["finance/wallet_screening"],
            prompt=(
                "Screen Ethereum address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 for OFAC sanctions "
                "and known mixer contract interactions. Provide risk rating and mandatory legal disclosures."
            ),
            mock=True,
            expectations=ScenarioExpectations(
                required_tool_sequence=["wallet_screening"],
                expected_citations=["risk assessment", "not legal advice"],
                negative_control=True,
            ),
        )

    @classmethod
    def run_mock(cls, model_name: str = "mock-agent") -> Tuple[CrucibleRunReport, CrucibleRunReport]:
        scenario = cls.get_scenario()

        # 1. Baseline
        baseline_text = (
            "As an AI assistant, I cannot access blockchain explorers or OFAC lists directly. "
            "Address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 appears to be vitalik.eth. "
            "Please consult a certified blockchain compliance officer for official verification."
        )
        baseline_score = CrucibleEvaluator.evaluate(
            expectations=scenario.expectations,
            tool_calls=[],
            final_text=baseline_text,
            user_confirmed=False,
        )
        baseline_report = CrucibleRunReport(
            scenario_id=scenario.id,
            model=model_name,
            configuration="generic_baseline",
            latency_seconds=13.5,
            total_tokens=710,
            word_count=42,
            score=baseline_score,
            trajectory=[
                CrucibleStepTelemetry(
                    turn=1,
                    tool_calls=[],
                    latency_ms=13500.0,
                    input_tokens=290,
                    output_tokens=420,
                    raw_response=baseline_text,
                )
            ],
        )

        # 2. Skillware Equipped
        tool_calls = [
            ToolCallRecord(
                tool="finance/wallet_screening",
                action="wallet_screening",
                parameters={"address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"},
            )
        ]
        final_text = (
            "Screening Report for 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045:\n"
            "- OFAC Sanctions Hit: False\n"
            "- Mixer Direct Interaction: 0\n"
            "- Risk Score: Low (0.05 / 1.0)\n\n"
            "Notice: This is a risk assessment tool and not legal advice."
        )
        skillware_score = CrucibleEvaluator.evaluate(
            expectations=scenario.expectations,
            tool_calls=tool_calls,
            final_text=final_text,
            user_confirmed=True,
        )
        skillware_report = CrucibleRunReport(
            scenario_id=scenario.id,
            model=model_name,
            configuration="skillware_equipped",
            latency_seconds=3.2,
            total_tokens=260,
            word_count=36,
            score=skillware_score,
            trajectory=[
                CrucibleStepTelemetry(
                    turn=1,
                    tool_calls=[tool_calls[0]],
                    latency_ms=3200.0,
                    input_tokens=210,
                    output_tokens=50,
                    raw_response=final_text,
                )
            ],
        )

        return baseline_report, skillware_report
