# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Unit tests for cryptographic Ed25519 provenance signing, trace verification, and compliance exports."""

import json
from pathlib import Path
from unittest.mock import MagicMock
from rich.console import Console

from skillware_bench.cli import cmd_export_compliance, cmd_verify
from skillware_bench.core.provenance import ProvenanceEngine, compute_event_hash


def _create_sample_trace(log_path: Path, event_count: int = 4) -> None:
    """Helper to generate a valid hash-chained .aura.jsonl log."""
    events = []
    prev_hash = None
    for i in range(event_count):
        ev = {
            "event_id": f"evt_{i:04d}",
            "parent_id": f"evt_{i-1:04d}" if i > 0 else None,
            "trace_id": "trace_test_123",
            "span_id": f"span_{i}",
            "step_id": f"step_{i}",
            "task_id": "task_root",
            "session_id": "session_test",
            "aura_id": "aura_bench_test",
            "agent_ids": {"model": "golden-target"},
            "kind": "constraint.approved" if i == 2 else "benchmark.turn",
            "timestamp": "2026-10-13T12:00:00Z",
            "payload": {"turn": i, "action": f"test_action_{i}"},
            "telemetry": {"latency_ms": 150.0},
        }
        content_hash = compute_event_hash(ev, prev_hash)
        ev["prev_hash"] = prev_hash
        ev["content_hash"] = content_hash
        prev_hash = content_hash
        events.append(ev)

    with log_path.open("w", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps(ev) + "\n")


def test_provenance_signing_and_verification(tmp_path: Path):
    trace_file = tmp_path / "test_session.aura.jsonl"
    _create_sample_trace(trace_file)

    # 1. Sign trace
    receipt = ProvenanceEngine.sign_trace(trace_file, model_name="test-model")
    assert receipt.event_count == 4
    assert len(receipt.signature_b64) > 20
    assert len(receipt.public_key_hex) == 64

    sig_file = trace_file.with_suffix(".sig")
    assert sig_file.exists()

    # 2. Verify trace with signature
    result = ProvenanceEngine.verify_trace(trace_file)
    assert result["valid"] is True
    assert result["hash_chain_valid"] is True
    assert result["signature_verified"] is True
    assert result["events_verified"] == 4
    assert result["verdict"] == "VERIFIED_AUTHENTIC"
    assert result["constitutional_approvals"] == 1


def test_provenance_tamper_detection(tmp_path: Path):
    trace_file = tmp_path / "tampered_session.aura.jsonl"
    _create_sample_trace(trace_file)
    ProvenanceEngine.sign_trace(trace_file, model_name="test-model")

    # Read, tamper with event 1, and write back
    lines = trace_file.read_text(encoding="utf-8").splitlines()
    tampered_event = json.loads(lines[1])
    tampered_event["payload"]["malicious_injection"] = True
    lines[1] = json.dumps(tampered_event)
    trace_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    result = ProvenanceEngine.verify_trace(trace_file)
    assert result["valid"] is False
    assert result["hash_chain_valid"] is False
    assert result["broken_event_id"] == "evt_0001"
    assert result["verdict"] == "VERIFICATION_FAILED"


def test_provenance_compliance_report_export(tmp_path: Path):
    trace_file = tmp_path / "compliance_session.aura.jsonl"
    _create_sample_trace(trace_file)
    ProvenanceEngine.sign_trace(trace_file, model_name="test-model")

    report_file = tmp_path / "compliance_report.json"
    report = ProvenanceEngine.export_compliance_report(trace_file, output_path=report_file)

    assert "standards" in report
    assert "EU_AI_Act_Article_14_1_Human_Oversight" in report["standards"]
    assert "ISO_IEC_42001_Clause_9_Trace_Reproducibility" in report["standards"]
    assert report["standards"]["EU_AI_Act_Article_14_1_Human_Oversight"]["status"] == "COMPLIANT"
    assert report_file.exists()


def test_cli_verify_and_compliance_commands(tmp_path: Path):
    trace_file = tmp_path / "cli_test_session.aura.jsonl"
    _create_sample_trace(trace_file)
    ProvenanceEngine.sign_trace(trace_file, model_name="test-model")

    console = Console(record=True, width=120)
    args = MagicMock()
    args.trace = str(trace_file)

    # 1. Test CLI verify
    cmd_verify(args, console)
    out_verify = console.export_text()
    assert "[PASS] Cryptographic Trace Verification Succeeded" in out_verify
    assert "Events Verified: 4" in out_verify
    assert "Ed25519 Signature: AUTHENTIC" in out_verify

    # 2. Test CLI export-compliance
    output_json = tmp_path / "out_compliance.json"
    args.output = str(output_json)
    console_comp = Console(record=True, width=120)
    cmd_export_compliance(args, console_comp)
    out_comp = console_comp.export_text()
    assert "AI Regulatory Oversight Assessment" in out_comp
    assert "EU AI Act" in out_comp
    assert output_json.exists()

    # 3. Test CLI audit
    from skillware_bench.cli import cmd_audit

    console_audit = Console(record=True, width=120)
    cmd_audit(args, console_audit)
    out_audit = console_audit.export_text()
    assert "Auditing AURA Causal Provenance Trace" in out_audit
    assert "Events Verified" in out_audit
    assert "AUTHENTIC" in out_audit


def test_provenance_report_verification(tmp_path: Path):
    import hashlib

    # 1. Valid report test
    report_data = {
        "run_id": "tiered_ablation_unit_test",
        "timestamp_utc": "20261027_120000",
        "model": "test-provider/test-model",
        "results": [
            {
                "configuration": "Vanilla Baseline",
                "scenario": "office_mail",
                "tier": 1,
                "success": True,
            },
            {
                "configuration": "Skillware Equipped",
                "scenario": "office_mail",
                "tier": 1,
                "success": True,
            },
        ],
    }
    canonical_json = json.dumps(report_data, indent=2, ensure_ascii=False)
    computed_hash = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
    report_data["aura_cryptographic_receipt"] = {
        "sha256": computed_hash,
        "engine": "AURA AuditSpine / SHA-256",
        "verified": True,
    }

    report_path = tmp_path / "test_report.json"
    report_path.write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8")

    res = ProvenanceEngine.verify_report(report_path)
    assert res["valid"] is True
    assert res["verdict"] == "AUTHENTIC"
    assert res["receipt_hash"] == computed_hash
    assert res["total_conditions"] == 2
    assert res["vanilla_pass"] == 1
    assert res["skillware_pass"] == 1

    # 2. Tampered report test (modifying success verdict)
    report_data["results"][0]["success"] = False
    tampered_path = tmp_path / "tampered_report.json"
    tampered_path.write_text(
        json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    tampered_res = ProvenanceEngine.verify_report(tampered_path)
    assert tampered_res["valid"] is False
    assert tampered_res["verdict"] == "HASH_MISMATCH"

    # 3. CLI verify on report test
    console = Console(record=True, width=120)
    args = MagicMock()
    args.trace = str(report_path)
    cmd_verify(args, console)
    out_verify = console.export_text()
    assert "[PASS] Benchmark Execution Report Verification Succeeded" in out_verify
    assert "AUTHENTIC / UNTAMPERED" in out_verify
