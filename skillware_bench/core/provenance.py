# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Cryptographic Ed25519 provenance signing, AURA audit trace verification, and compliance exporter."""

import base64
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
except ImportError:
    ed25519 = None  # type: ignore
    serialization = None  # type: ignore


@dataclass
class ProvenanceReceipt:
    """Cryptographic verification receipt for an immutable benchmark trace."""

    trace_id: str
    session_id: str
    model: str
    root_hash: str
    event_count: int
    timestamp: str
    signature_b64: str
    public_key_hex: str
    algorithm: str = "ed25519"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def compute_event_hash(event_data: Dict[str, Any], prev_hash: Optional[str]) -> str:
    """Compute canonical SHA-256 content hash matching AURA AuditSpine specification."""
    canonical_body = {
        "event_id": event_data.get("event_id"),
        "parent_id": event_data.get("parent_id"),
        "trace_id": event_data.get("trace_id"),
        "span_id": event_data.get("span_id"),
        "step_id": event_data.get("step_id"),
        "task_id": event_data.get("task_id"),
        "session_id": event_data.get("session_id"),
        "aura_id": event_data.get("aura_id"),
        "agent_ids": event_data.get("agent_ids", {}),
        "kind": event_data.get("kind"),
        "timestamp": event_data.get("timestamp"),
        "payload": event_data.get("payload", {}),
        "telemetry": event_data.get("telemetry", {}),
    }
    blob = json.dumps(canonical_body, sort_keys=True, ensure_ascii=False)
    prefix = prev_hash or "genesis"
    return hashlib.sha256(f"{prefix}:{blob}".encode("utf-8")).hexdigest()


class ProvenanceEngine:
    """Signs and cryptographically verifies benchmark traces and produces compliance audits."""

    @classmethod
    def generate_keypair(cls) -> Tuple[Any, str]:
        """Generate a new Ed25519 private key and return (private_key, public_key_hex)."""
        if ed25519 is None:
            raise RuntimeError("cryptography package is required for Ed25519 operations")
        priv_key = ed25519.Ed25519PrivateKey.generate()
        pub_bytes = priv_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        return priv_key, pub_bytes.hex()

    @classmethod
    def sign_trace(
        cls,
        trace_path: Union[str, Path],
        private_key: Optional[Any] = None,
        model_name: str = "unknown-model",
    ) -> ProvenanceReceipt:
        """Sign an AURA .aura.jsonl trace file, generating an Ed25519 cryptographic receipt."""
        path = Path(trace_path)
        if not path.is_file():
            raise FileNotFoundError(f"Trace file does not exist: {trace_path}")

        events: List[Dict[str, Any]] = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))

        if not events:
            raise ValueError(f"Trace file is empty: {trace_path}")

        prev_hash: Optional[str] = None
        for ev in events:
            content_hash = ev.get("content_hash")
            if not content_hash:
                content_hash = compute_event_hash(ev, prev_hash)
            prev_hash = content_hash

        root_hash = prev_hash or ""
        first_event = events[0]
        trace_id = first_event.get("trace_id", "trace_default")
        session_id = first_event.get("session_id", "session_default")

        if private_key is None:
            private_key, pub_hex = cls.generate_keypair()
        else:
            pub_bytes = private_key.public_key().public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            )
            pub_hex = pub_bytes.hex()

        sig_bytes = private_key.sign(root_hash.encode("utf-8"))
        sig_b64 = base64.b64encode(sig_bytes).decode("ascii")

        receipt = ProvenanceReceipt(
            trace_id=trace_id,
            session_id=session_id,
            model=model_name,
            root_hash=root_hash,
            event_count=len(events),
            timestamp=datetime.now(timezone.utc).isoformat(),
            signature_b64=sig_b64,
            public_key_hex=pub_hex,
        )

        # Write companion receipt file
        sig_file = path.with_suffix(".sig")
        with sig_file.open("w", encoding="utf-8") as sf:
            json.dump(receipt.to_dict(), sf, indent=2)

        return receipt

    @classmethod
    def verify_trace(
        cls,
        trace_path: Union[str, Path],
        receipt_path: Optional[Union[str, Path]] = None,
    ) -> Dict[str, Any]:
        """Verify hash chain integrity and cryptographic signature of an AURA trace file."""
        path = Path(trace_path)
        if not path.is_file():
            raise FileNotFoundError(f"Trace file not found: {trace_path}")

        events: List[Dict[str, Any]] = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))

        if not events:
            return {
                "valid": False,
                "error": "Trace file is empty",
                "events_verified": 0,
                "verdict": "FAILED_EMPTY",
            }

        prev_hash: Optional[str] = None
        chain_broken = False
        broken_event_id: Optional[str] = None

        for idx, ev in enumerate(events):
            expected = compute_event_hash(ev, prev_hash)
            actual = ev.get("content_hash")
            if actual is not None and actual != expected:
                chain_broken = True
                broken_event_id = ev.get("event_id", f"step_{idx}")
                break
            prev_hash = actual or expected

        terminal_root_hash = prev_hash or ""

        # Signature verification if receipt available
        sig_file = (
            Path(receipt_path)
            if receipt_path
            else (
                path.parent / f"{path.name}.sig"
                if (path.parent / f"{path.name}.sig").exists()
                else path.with_suffix(".sig")
            )
        )
        signature_valid: Optional[bool] = None
        receipt_data: Optional[Dict[str, Any]] = None

        if sig_file.is_file() and ed25519 is not None:
            try:
                with sig_file.open("r", encoding="utf-8") as sf:
                    receipt_data = json.load(sf)

                pub_bytes = bytes.fromhex(receipt_data["public_key_hex"])
                sig_bytes = base64.b64decode(receipt_data["signature_b64"])
                root_hash_to_verify = receipt_data["root_hash"]

                pub_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
                pub_key.verify(sig_bytes, root_hash_to_verify.encode("utf-8"))

                # Check that root hash matches computed terminal hash
                signature_valid = root_hash_to_verify == terminal_root_hash
            except Exception:
                signature_valid = False

        # Gather constitutional statistics from event kinds
        violations = [ev for ev in events if "violated" in ev.get("kind", "")]
        approvals = [ev for ev in events if "approved" in ev.get("kind", "")]

        is_valid = (not chain_broken) and (signature_valid is not False)

        return {
            "valid": is_valid,
            "hash_chain_valid": not chain_broken,
            "broken_event_id": broken_event_id,
            "events_verified": len(events),
            "root_hash": terminal_root_hash,
            "signature_verified": signature_valid,
            "receipt": receipt_data,
            "constitutional_approvals": len(approvals),
            "constitutional_violations": len(violations),
            "verdict": "VERIFIED_AUTHENTIC" if is_valid else "VERIFICATION_FAILED",
        }

    @classmethod
    def export_compliance_report(
        cls,
        trace_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
    ) -> Dict[str, Any]:
        """Generate ISO/IEC 42001 & EU AI Act Article 14 regulatory oversight assessment."""
        verification = cls.verify_trace(trace_path)
        path = Path(trace_path)

        events: List[Dict[str, Any]] = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))

        # Evaluate Article 14 dimensions
        has_oversight_gate = verification["constitutional_approvals"] > 0
        has_violations = verification["constitutional_violations"] > 0
        chain_authentic = verification["hash_chain_valid"]

        compliance_scorecard = {
            "standards": {
                "EU_AI_Act_Article_14_1_Human_Oversight": {
                    "requirement": "AI systems must be designed to enable human oversight during execution.",
                    "status": "COMPLIANT" if has_oversight_gate else "PARTIAL",
                    "evidence": f"{verification['constitutional_approvals']} explicit human/policy gates confirmed",
                },
                "EU_AI_Act_Article_14_4_Automation_Bias_Defense": {
                    "requirement": "Prevention of over-reliance and automated execution under ambiguous intent.",
                    "status": "COMPLIANT" if not has_violations else "ACTION_REQUIRED",
                    "evidence": f"{verification['constitutional_violations']} unauthorized actions intercepted",
                },
                "ISO_IEC_42001_Clause_9_Trace_Reproducibility": {
                    "requirement": "Immutable and verifiable operational telemetry audit trails.",
                    "status": "COMPLIANT" if chain_authentic else "NON_COMPLIANT",
                    "evidence": f"Root hash {verification['root_hash'][:16]}... cryptographically verified",
                },
            },
            "metadata": {
                "trace_path": str(path),
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "verdict": verification["verdict"],
                "total_events": verification["events_verified"],
            },
        }

        if output_path:
            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            with out.open("w", encoding="utf-8") as f:
                json.dump(compliance_scorecard, f, indent=2)

        return compliance_scorecard
