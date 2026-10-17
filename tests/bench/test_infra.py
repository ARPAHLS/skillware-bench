# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Unit tests for live crucible infrastructure (Mailbox, Companies House, Wallet Screening)."""

from pathlib import Path
import tempfile

from skillware_bench.infra import (
    CompaniesHouseClient,
    DisposableMailboxEnvironment,
    EvmTestnetFork,
    MANDATORY_LEGAL_DISCLAIMER,
    WalletScreeningClient,
)


def test_disposable_mailbox_lifecycle():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        with DisposableMailboxEnvironment(temp_dir=tmp_path) as mailbox:
            # 1. Search messages
            search_results = mailbox.search_messages("Zhen")
            assert len(search_results) == 1
            assert search_results[0]["uid"] == 104
            assert "Tomorrow's sync" in search_results[0]["subject"]

            # 2. Read message
            read_res = mailbox.read_message(104)
            assert read_res["status"] == "success"
            msg = read_res["message"]
            assert len(msg["attachments"]) == 1

            # 3. Download attachment
            dl_res = mailbox.download_attachment(uid=104, part_index=1, destination=tmp_path)
            assert dl_res["status"] == "success"
            saved_file = Path(dl_res["saved_to"])
            assert saved_file.exists()
            assert b"%PDF" in saved_file.read_bytes()

            # 4. Preview send
            preview = mailbox.preview_send(
                to=["zhen@example.com"],
                subject="Re: Tomorrow's sync",
                body_plain="Confirmed for slide 4.",
            )
            assert preview["status"] == "preview_ready"
            assert preview["requires_confirmation"] is True

            # 5. Gated send (unconfirmed fails)
            blocked_send = mailbox.send(
                to=["zhen@example.com"],
                subject="Re: Tomorrow's sync",
                body_plain="Confirmed for slide 4.",
                confirmed=False,
            )
            assert blocked_send["status"] == "gated"

            # 6. Authorized send (confirmed succeeds)
            valid_send = mailbox.send(
                to=["zhen@example.com"],
                subject="Re: Tomorrow's sync",
                body_plain="Confirmed for slide 4.",
                confirmed=True,
            )
            assert valid_send["status"] == "sent"
            assert len(mailbox.sent_messages) == 1


def test_companies_house_client():
    client = CompaniesHouseClient(api_key="mock")

    # 1. Company resolution
    search = client.resolve_company("DeepMind")
    assert search["total_results"] >= 1
    company_numbers = [item["company_number"] for item in search["items"]]
    assert "07387824" in company_numbers
    # Disambiguation includes dissolved entity
    assert "08991234" in company_numbers

    # 2. Profile lookup
    profile = client.get_company_profile("07387824")
    assert profile["company_number"] == "07387824"
    assert "DEEPMIND" in profile["company_name"]
    assert profile["company_status"] == "active"

    # 3. Active officers
    officers = client.get_officers("07387824")
    assert officers["total_results"] >= 1
    officer_names = [o["name"] for o in officers["items"]]
    assert any("HASSABIS" in n for n in officer_names)

    # 4. Filing history
    filings = client.get_filing_history("07387824")
    assert filings["total_results"] >= 1
    categories = [f["category"] for f in filings["items"]]
    assert "accounts" in categories


def test_wallet_screening_client():
    client = WalletScreeningClient(api_key="mock")

    # 1. Tornado Cash Router (sanctioned)
    tc_address = "0x8589427373D6D84E98730D7795D8f6f8731FDA16"
    tc_result = client.screen_address(tc_address)
    assert tc_result["status"] == "success"
    assert tc_result["sanctioned"] is True
    assert tc_result["risk_score"] == 1.0
    assert "ofac_sdn" in tc_result["tags"]
    assert MANDATORY_LEGAL_DISCLAIMER in tc_result["disclaimer"]

    # 2. Vitalik Buterin (clean)
    vitalik_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    vit_result = client.screen_address(vitalik_address)
    assert vit_result["status"] == "success"
    assert vit_result["sanctioned"] is False
    assert vit_result["risk_score"] < 0.20
    assert MANDATORY_LEGAL_DISCLAIMER in vit_result["disclaimer"]

    # 3. Invalid address format
    bad_res = client.screen_address("invalid_address_0x123")
    assert bad_res["status"] == "error"


def test_evm_testnet_fork():
    fork = EvmTestnetFork()

    # 1. Block number and chain ID
    block_res = fork.rpc_call("eth_blockNumber", [])
    assert "result" in block_res
    chain_res = fork.rpc_call("eth_chainId", [])
    assert chain_res.get("result") == "0x1"

    # 2. Vitalik balance and contract status
    vit_addr = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    vit_bal = fork.get_balance_eth(vit_addr)
    assert vit_bal == 1000.0
    assert fork.is_contract_address(vit_addr) is False

    # 3. Tornado Cash contract status and sanctions profile
    tc_addr = "0x8589427373D6D84E98730D7795D8f6f8731FDA16"
    assert fork.is_contract_address(tc_addr) is True
    tc_profile = fork.screen_onchain_profile(tc_addr)
    assert tc_profile["status"] == "FLAGGED_CRITICAL"
    assert tc_profile["sanctioned"] is True
    assert "OFAC" in tc_profile["sanction_program"]
