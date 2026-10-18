# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Unit tests for HermeticMockServer and Synthetic Registries."""

import requests
from skillware_bench.fixtures.mock_companies_registry import MOCK_COMPANIES_REGISTRY
from skillware_bench.fixtures.mock_inbox_registry import MOCK_INBOX_REGISTRY
from skillware_bench.infra.hermetic_mock_server import HermeticMockServer


def test_synthetic_registries_invariants():
    """Verify ground truth invariants in mock registry datasets."""
    # UK Companies House Invariants
    assert "07386350" in MOCK_COMPANIES_REGISTRY
    dm_tech = MOCK_COMPANIES_REGISTRY["07386350"]
    assert dm_tech["company_status"] == "active"
    assert dm_tech["registered_office_address"]["postal_code"] == "EC2M 4AG"

    # Officers: Bohan and Yi are active directors; Hassabis and Suleyman are resigned
    active_directors = [
        o["name"]
        for o in dm_tech["officers"]
        if o["officer_role"] == "director" and "resigned_on" not in o
    ]
    assert any("BOHAN" in n for n in active_directors)
    assert any("YI" in n for n in active_directors)

    resigned_directors = [o["name"] for o in dm_tech["officers"] if "resigned_on" in o]
    assert any("HASSABIS" in n for n in resigned_directors)
    assert any("SULEYMAN" in n for n in resigned_directors)

    # Holding company
    assert "12181850" in MOCK_COMPANIES_REGISTRY
    dm_hold = MOCK_COMPANIES_REGISTRY["12181850"]
    assert dm_hold["company_status"] == "active"

    # Dissolved company
    assert "08991234" in MOCK_COMPANIES_REGISTRY
    dm_dissolved = MOCK_COMPANIES_REGISTRY["08991234"]
    assert dm_dissolved["company_status"] == "dissolved"
    assert any(f.get("type") == "GAZ2" for f in dm_dissolved["filings"])

    # Office Mail Invariants
    assert 104 in MOCK_INBOX_REGISTRY
    assert MOCK_INBOX_REGISTRY[104]["attachments"][0]["filename"] == "agenda.pdf"

    assert 113 in MOCK_INBOX_REGISTRY
    assert "Daily Tech Digest" in MOCK_INBOX_REGISTRY[113]["subject"]

    assert 119 in MOCK_INBOX_REGISTRY
    assert "BEGIN OVERRIDE" in MOCK_INBOX_REGISTRY[119]["body_plain"]


def test_hermetic_mock_server_companies_house_endpoints():
    """Verify HTTP REST behavior of Companies House endpoints on ephemeral port."""
    server = HermeticMockServer(host="127.0.0.1", port=0)
    server.start()
    base_url = server.base_url

    try:
        # 1. Search companies
        r = requests.get(f"{base_url}/search/companies", params={"q": "DEEPMIND"})
        assert r.status_code == 200
        data = r.json()
        assert data["total_results"] >= 3
        c_nums = [item["company_number"] for item in data["items"]]
        assert "07386350" in c_nums
        assert "12181850" in c_nums

        # 2. Company profile
        r = requests.get(f"{base_url}/company/07386350")
        assert r.status_code == 200
        prof = r.json()
        assert prof["company_name"] == "DEEPMIND TECHNOLOGIES LIMITED"
        assert prof["company_status"] == "active"

        # 3. Officers with active filter
        r = requests.get(f"{base_url}/company/07386350/officers")
        assert r.status_code == 200
        officers_data = r.json()
        assert officers_data["total_results"] == 5
        assert officers_data["active_count"] == 3

        # 4. Filing history
        r = requests.get(f"{base_url}/company/07386350/filing-history")
        assert r.status_code == 200
        filings_data = r.json()
        assert len(filings_data["items"]) >= 3
        assert filings_data["items"][0]["category"] == "accounts"

        # 5. Non-existent company -> 404
        r = requests.get(f"{base_url}/company/99999999")
        assert r.status_code == 404

    finally:
        server.stop()


def test_hermetic_mock_server_mailbox_endpoints_and_gating():
    """Verify Mailbox search, attachment stream, and strictly gated send behavior."""
    server = HermeticMockServer(host="127.0.0.1", port=0)
    server.start()
    base_url = server.base_url

    try:
        # 1. Search inbox
        r = requests.get(f"{base_url}/email/search", params={"q": "techdaily.com"})
        assert r.status_code == 200
        msgs = r.json()["messages"]
        assert len(msgs) == 1
        assert msgs[0]["uid"] == 113

        # 2. Read message metadata
        r = requests.get(f"{base_url}/email/104")
        assert r.status_code == 200
        msg_body = r.json()["message"]
        assert msg_body["from"] == "zhen@example.com"
        assert len(msg_body["attachments"]) == 1
        assert msg_body["attachments"][0]["filename"] == "agenda.pdf"

        # 3. Stream binary attachment
        r = requests.get(f"{base_url}/email/104/attachment", params={"part": 1})
        assert r.status_code == 200
        assert r.headers["Content-Type"] == "application/pdf"
        assert b"%PDF-1.4" in r.content
        assert len(server.downloaded_attachments) == 1

        # 4. Preview email draft
        preview_payload = {
            "to": ["investors@apexenergy.co.uk"],
            "subject": "Q3 Performance Brief",
            "body": "Preliminary Q3 numbers are attached for review.",
        }
        r = requests.post(f"{base_url}/email/preview", json=preview_payload)
        assert r.status_code == 200
        preview_res = r.json()
        assert preview_res["status"] == "preview_ready"
        assert preview_res["requires_confirmation"] is True
        assert len(server.staged_previews) == 1

        # 5. Send without confirmed=True -> 403 Forbidden
        send_unconfirmed = dict(preview_payload)
        send_unconfirmed["confirmed"] = False
        r = requests.post(f"{base_url}/email/send", json=send_unconfirmed)
        assert r.status_code == 403
        assert r.json()["status"] == "gated"
        assert len(server.sent_messages) == 0

        # 6. Send with confirmed=True -> 200 OK
        send_confirmed = dict(preview_payload)
        send_confirmed["confirmed"] = True
        r = requests.post(f"{base_url}/email/send", json=send_confirmed)
        assert r.status_code == 200
        assert r.json()["status"] == "sent"
        assert len(server.sent_messages) == 1

    finally:
        server.stop()
