# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""UK Companies House simulation crucible (finance/uk_companies_house_handler)."""

from typing import Tuple
from skillware_bench.core.adapters.base import BaseModelAdapter
from skillware_bench.core.agent_loop import AgentLoop
from skillware_bench.core.evaluators import CrucibleEvaluator
from skillware_bench.core.models import (
    CrucibleRunReport,
    CrucibleStepTelemetry,
    EvalTier,
    ScenarioDefinition,
    ScenarioExpectations,
    ToolCallRecord,
)
from skillware_bench.infra import CompaniesHouseClient


class CompaniesHouseCrucible:
    """Evaluates agent execution of corporate entity resolution and filing audits."""

    @classmethod
    def get_scenario(cls) -> ScenarioDefinition:
        return ScenarioDefinition(
            id="finance_companies_house_01",
            title="UK Corporate Intelligence: Entity Disambiguation & Officer Audit",
            tier=EvalTier.TIER_3_CONSTITUTION,
            category="finance",
            skills=["finance/uk_companies_house_handler"],
            prompt=(
                "Look up 'DeepMind Technologies' on UK Companies House. "
                "Disambiguate the active registered company number, list the active directors, "
                "and find the latest filing category."
            ),
            mock=True,
            expectations=ScenarioExpectations(
                required_tool_sequence=["resolve_company", "get_officers", "get_filing_history"],
                expected_citations=["07387824"],
                negative_control=True,
            ),
        )

    @classmethod
    def run_mock(
        cls, model_name: str = "mock-agent"
    ) -> Tuple[CrucibleRunReport, CrucibleRunReport]:
        scenario = cls.get_scenario()

        # 1. Baseline
        baseline_text = (
            "DeepMind Technologies is a UK artificial intelligence company founded in 2010. "
            "Its company registration number is approximately 07387800 (or similar). "
            "Please consult the official Companies House WebCheck portal as I do not have "
            "real-time access to the UK government API registry to verify active directors."
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
            latency_seconds=11.2,
            total_tokens=680,
            word_count=48,
            score=baseline_score,
            trajectory=[
                CrucibleStepTelemetry(
                    turn=1,
                    tool_calls=[],
                    latency_ms=11200.0,
                    input_tokens=320,
                    output_tokens=360,
                    raw_response=baseline_text,
                )
            ],
        )

        # 2. Skillware Equipped
        tool_calls = [
            ToolCallRecord(
                tool="finance/uk_companies_house_handler",
                action="resolve_company",
                parameters={"query": "DeepMind Technologies"},
            ),
            ToolCallRecord(
                tool="finance/uk_companies_house_handler",
                action="get_officers",
                parameters={"company_number": "07387824", "active_only": True},
            ),
            ToolCallRecord(
                tool="finance/uk_companies_house_handler",
                action="get_filing_history",
                parameters={"company_number": "07387824", "latest_only": True},
            ),
        ]
        final_text = (
            "DeepMind Technologies Limited resolved to registered company number 07387824 (Active). "
            "Active officers include Demis Hassabis and corporate secretaries. "
            "Latest filing category: accounts (fetched_at: 2026-10-13T10:00:00Z)."
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
            latency_seconds=4.1,
            total_tokens=320,
            word_count=34,
            score=skillware_score,
            trajectory=[
                CrucibleStepTelemetry(
                    turn=1,
                    tool_calls=[tool_calls[0]],
                    latency_ms=1200.0,
                    input_tokens=210,
                    output_tokens=40,
                    raw_response="Resolved company number: 07387824.",
                ),
                CrucibleStepTelemetry(
                    turn=2,
                    tool_calls=[tool_calls[1], tool_calls[2]],
                    latency_ms=2900.0,
                    input_tokens=350,
                    output_tokens=70,
                    raw_response=final_text,
                ),
            ],
        )

        return baseline_report, skillware_report

    @classmethod
    def run_live(
        cls, model_name: str, adapter: BaseModelAdapter
    ) -> Tuple[CrucibleRunReport, CrucibleRunReport]:
        scenario = cls.get_scenario()
        client = CompaniesHouseClient()

        # 1. Baseline unequipped run
        baseline_loop = AgentLoop(
            adapter=adapter,
            skill_names=[],
            system_prompt="You are an AI assistant. Answer the corporate intelligence prompt as best you can.",
            mock=False,
        )
        baseline_report = baseline_loop.run(
            prompt=scenario.prompt,
            scenario=scenario,
            expectations=scenario.expectations,
        )
        baseline_report.configuration = "generic_baseline"

        # 2. Skillware equipped run with live Companies House client
        equipped_loop = AgentLoop(
            adapter=adapter,
            skill_names=scenario.skills,
            infra_handlers={
                "finance/uk_companies_house_handler": client,
                "uk_companies_house_handler": client,
                "companies_house": client,
            },
            system_prompt=(
                "You are an enterprise AI agent equipped with Skillware "
                "finance/uk_companies_house_handler. Disambiguate company numbers "
                "carefully and cite exact registration numbers and director names."
            ),
            mock=False,
        )
        skillware_report = equipped_loop.run(
            prompt=scenario.prompt,
            scenario=scenario,
            expectations=scenario.expectations,
        )
        skillware_report.configuration = "skillware_equipped"

        return baseline_report, skillware_report
