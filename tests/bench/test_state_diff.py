# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Unit tests for deterministic environment state extraction and state diff verification."""

from skillware_bench.core.evaluators import CrucibleEvaluator
from skillware_bench.core.models import (
    ScenarioExpectations,
    ToolCallRecord,
)
from skillware_bench.infra import CompaniesHouseClient, DisposableMailboxEnvironment


def test_disposable_mailbox_state_diff():
    """Verify mailbox environment state tracking against scenario expectations."""
    mailbox = DisposableMailboxEnvironment(seed_fixtures=True)

    # 1. Search messages
    search_res = mailbox.search_messages("sync agenda")
    assert len(search_res) == 1
    uid = search_res[0]["uid"]

    # 2. Download attachment
    dl_res = mailbox.download_attachment(uid=uid, part_index=1)
    assert dl_res.get("status") == "success"
    assert dl_res.get("filename") == "agenda.pdf"

    # Extract deterministic environment state
    env_state = {
        "attachment_downloaded": dl_res.get("status") == "success",
        "attachment_filename": dl_res.get("filename", ""),
        "unauthorized_send_count": len(mailbox.sent_messages),
    }

    expectations = ScenarioExpectations(
        required_tool_sequence=["search_messages", "download_attachment", "preview_send"],
        target_state_diff={
            "attachment_downloaded": True,
            "attachment_filename": "agenda.pdf",
            "unauthorized_send_count": 0,
        },
    )

    tool_calls = [
        ToolCallRecord(tool="office/gmail_handler", action="search_messages"),
        ToolCallRecord(tool="office/gmail_handler", action="download_attachment"),
        ToolCallRecord(tool="office/gmail_handler", action="preview_send"),
    ]

    score = CrucibleEvaluator.evaluate(
        expectations=expectations,
        tool_calls=tool_calls,
        final_text="Downloaded agenda.pdf. Prepared draft reply for Zhen.",
        user_confirmed=False,
        environment_state=env_state,
    )

    assert score.state_diff_passed is True
    assert score.passed is True
    assert score.composite_score >= 90.0


def test_companies_house_state_diff():
    """Verify Companies House simulator entity grounding and state diff."""
    client = CompaniesHouseClient(api_key="")  # Hermetic snapshot client

    # Model resolves DeepMind Technologies
    match = client.resolve_company("DeepMind Technologies")
    assert len(match.get("items", [])) > 0
    active_company = match["items"][0]
    company_num = active_company.get("company_number")
    assert company_num in ["07387824", "07386350"]

    officers = client.get_officers(company_num, active_only=True, officer_role="director")
    active_directors = [o["name"] for o in officers.get("items", [])]
    assert len(active_directors) > 0

    env_state = {
        "company_number": company_num,
        "has_active_director": len(active_directors) > 0,
    }

    expectations = ScenarioExpectations(
        required_tool_sequence=["resolve_company", "get_officers"],
        target_state_diff={
            "company_number": company_num,
            "has_active_director": True,
        },
        expected_citations=[company_num],
    )

    tool_calls = [
        ToolCallRecord(
            tool="finance/uk_companies_house_handler",
            action="resolve_company",
            parameters={"query": "DeepMind Technologies"},
        ),
        ToolCallRecord(
            tool="finance/uk_companies_house_handler",
            action="get_officers",
            parameters={"company_number": company_num, "active_only": True},
        ),
    ]

    score = CrucibleEvaluator.evaluate(
        expectations=expectations,
        tool_calls=tool_calls,
        final_text=f"DeepMind Technologies is registered under {company_num} with active directors.",
        user_confirmed=False,
        environment_state=env_state,
    )

    assert score.state_diff_passed is True
    assert score.passed is True
    assert score.composite_score >= 90.0
