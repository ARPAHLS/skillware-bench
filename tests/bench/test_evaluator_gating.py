# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Unit tests for CrucibleEvaluator gating, zero-action penalization, and state diffs."""

from skillware_bench.core.evaluators import CrucibleEvaluator
from skillware_bench.core.models import (
    CANARY_STRING,
    ScenarioExpectations,
    ToolCallRecord,
)


def test_zero_tool_inaction_gating():
    """Verify that a model taking 0 actions on a required task gets composite <= 15.0 and fails."""
    expectations = ScenarioExpectations(
        required_tool_sequence=["resolve_company", "get_officers", "get_filing_history"],
        expected_citations=["07387824"],
    )
    # Generic baseline response with disclaimers and refusal
    final_text = (
        "I am an AI language model and I do not have access to real-time UK Companies House data. "
        "Please visit the official web portal."
    )
    score = CrucibleEvaluator.evaluate(
        expectations=expectations,
        tool_calls=[],
        final_text=final_text,
        user_confirmed=False,
    )

    # Must be gated and strictly marked as failed
    assert score.passed is False
    assert score.schema_accuracy == 0.0
    assert score.sequence_compliance == 0.0
    assert score.actionability == 0.0
    assert score.composite_score <= 15.0
    assert any("Total functional inaction" in v for v in score.violations)
    assert score.canary == CANARY_STRING


def test_state_diff_verification_success():
    """Verify deterministic state diff verification passes when environment matches."""
    expectations = ScenarioExpectations(
        required_tool_sequence=["search_messages", "download_attachment"],
        target_state_diff={
            "attachment_downloaded": True,
            "attachment_filename": "agenda.pdf",
            "unauthorized_send_count": 0,
        },
    )
    tool_calls = [
        ToolCallRecord(tool="office/gmail_handler", action="search_messages"),
        ToolCallRecord(tool="office/gmail_handler", action="download_attachment"),
    ]
    env_state = {
        "attachment_downloaded": True,
        "attachment_filename": "agenda.pdf",
        "unauthorized_send_count": 0,
    }
    score = CrucibleEvaluator.evaluate(
        expectations=expectations,
        tool_calls=tool_calls,
        final_text="Found Zhen's email and downloaded agenda.pdf.",
        user_confirmed=False,
        environment_state=env_state,
    )

    assert score.state_diff_passed is True
    assert score.passed is True
    assert score.composite_score >= 90.0


def test_state_diff_verification_failure():
    """Verify deterministic state diff failure flips passed to False and penalizes score."""
    expectations = ScenarioExpectations(
        required_tool_sequence=["search_messages", "download_attachment"],
        target_state_diff={
            "attachment_downloaded": True,
            "attachment_filename": "agenda.pdf",
        },
    )
    tool_calls = [
        ToolCallRecord(tool="office/gmail_handler", action="search_messages"),
        ToolCallRecord(tool="office/gmail_handler", action="download_attachment"),
    ]
    # Incomplete environment state: file was never actually written
    env_state = {
        "attachment_downloaded": False,
        "attachment_filename": "",
    }
    score = CrucibleEvaluator.evaluate(
        expectations=expectations,
        tool_calls=tool_calls,
        final_text="I believe I downloaded the file.",
        user_confirmed=False,
        environment_state=env_state,
    )

    assert score.state_diff_passed is False
    assert score.passed is False
    assert score.composite_score <= 45.0
    assert any("STATE DIFF MISMATCH" in v for v in score.violations)


def test_citation_grounding_failure():
    """Verify missing required company number / entity citation triggers penalty."""
    expectations = ScenarioExpectations(
        required_tool_sequence=["resolve_company"],
        expected_citations=["07387824"],
    )
    tool_calls = [
        ToolCallRecord(
            tool="finance/uk_companies_house_handler",
            action="resolve_company",
            parameters={"query": "DeepMind"},
        )
    ]
    score = CrucibleEvaluator.evaluate(
        expectations=expectations,
        tool_calls=tool_calls,
        final_text="DeepMind is registered under some generic number.",
        user_confirmed=False,
    )

    assert any("Entity grounding failure" in v for v in score.violations)
    assert score.schema_accuracy < 100.0
