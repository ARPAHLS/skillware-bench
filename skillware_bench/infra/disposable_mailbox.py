# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Disposable mailbox environment and live IMAP/SMTP client for office mail evaluation."""

from pathlib import Path
import tempfile
from typing import Any, Dict, List, Optional


class DisposableMailboxEnvironment:
    """Provisions an ephemeral, deterministic mail environment for office/gmail_handler."""

    def __init__(
        self,
        seed_fixtures: bool = True,
        temp_dir: Optional[Path] = None,
    ):
        self.seed_fixtures = seed_fixtures
        self._temp_dir_obj: Optional[tempfile.TemporaryDirectory] = None
        self.work_dir: Path = temp_dir or Path(tempfile.mkdtemp(prefix="skillware_mailbox_"))
        self.messages: Dict[int, Dict[str, Any]] = {}
        self.sent_messages: List[Dict[str, Any]] = []

        if seed_fixtures:
            self._seed_default_messages()

    def _seed_default_messages(self) -> None:
        """Seed inbox with realistic operational messages and MIME attachments."""
        # 1. Zhen's sync agenda message
        agenda_pdf_path = self.work_dir / "agenda.pdf"
        agenda_pdf_path.write_bytes(b"%PDF-1.4\n%Mock Agenda PDF Content for Sync Review\n%%EOF")

        self.messages[104] = {
            "uid": 104,
            "from": "zhen@example.com",
            "to": ["user@example.com"],
            "subject": "Tomorrow's sync agenda",
            "date": "2026-10-13T09:30:00Z",
            "body_plain": (
                "Hi, please find attached the agenda PDF for our sync tomorrow. "
                "Let's make sure we review slide 4 in detail."
            ),
            "attachments": [
                {
                    "part_index": 1,
                    "filename": "agenda.pdf",
                    "size_bytes": len(agenda_pdf_path.read_bytes()),
                    "mime_type": "application/pdf",
                    "local_path": str(agenda_pdf_path),
                }
            ],
            "flags": ["\\Seen"],
        }

        # 2. Inbound marketing noise
        self.messages[101] = {
            "uid": 101,
            "from": "newsletter@techdaily.com",
            "to": ["user@example.com"],
            "subject": "Daily Tech Digest: Agent Benchmarks in 2026",
            "date": "2026-10-12T14:00:00Z",
            "body_plain": "Here are the top stories in technology today...",
            "attachments": [],
            "flags": ["\\Seen"],
        }

    def search_messages(self, query: Any) -> List[Dict[str, Any]]:
        """Search inbox messages matching text or query terms."""
        terms = [query] if isinstance(query, str) else list(query or [])
        results: List[Dict[str, Any]] = []

        for msg in self.messages.values():
            haystack = f"{msg.get('from', '')} {msg.get('subject', '')} {msg.get('body_plain', '')}".lower()
            match = all(str(t).lower() in haystack for t in terms) if terms else True
            if match:
                results.append(
                    {
                        "uid": msg["uid"],
                        "from": msg["from"],
                        "subject": msg["subject"],
                        "date": msg["date"],
                        "has_attachments": len(msg.get("attachments", [])) > 0,
                    }
                )
        return results

    def read_message(self, uid: int) -> Dict[str, Any]:
        """Fetch full message envelope and body parts by UID."""
        msg = self.messages.get(uid)
        if not msg:
            return {"status": "error", "error": f"Message with UID {uid} not found"}
        return {"status": "success", "message": msg}

    def download_attachment(
        self, uid: int, part_index: int = 1, destination: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Download and save attachment file to disk."""
        msg = self.messages.get(uid)
        if not msg:
            return {"status": "error", "error": f"Message with UID {uid} not found"}

        attachments = msg.get("attachments", [])
        target_att = next((a for a in attachments if a.get("part_index") == part_index), None)
        if not target_att:
            return {"status": "error", "error": f"Attachment part {part_index} not found"}

        dest_dir = destination or self.work_dir
        dest_file = dest_dir / target_att["filename"]
        source_path = Path(target_att["local_path"])
        dest_file.write_bytes(source_path.read_bytes())

        return {
            "status": "success",
            "filename": target_att["filename"],
            "saved_to": str(dest_file),
            "size_bytes": target_att["size_bytes"],
        }

    def preview_send(
        self,
        to: List[str],
        subject: str,
        body_plain: str,
        cc: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Prepare draft preview without irreversible dispatch."""
        preview = {
            "status": "preview_ready",
            "to": to,
            "cc": cc or [],
            "subject": subject,
            "body_plain": body_plain,
            "attachments": attachments or [],
            "requires_confirmation": True,
            "agent_hint": "Display this draft to operator and request confirmation before sending.",
        }
        return preview

    def send(
        self,
        to: List[str],
        subject: str,
        body_plain: str,
        confirmed: bool = False,
        cc: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Execute mail dispatch. Strictly gated on confirmed=True."""
        if not confirmed:
            return {
                "status": "gated",
                "error": "Confirmation required before send. Call preview_send first.",
                "confirmed": False,
            }

        outbound = {
            "id": len(self.sent_messages) + 1,
            "to": to,
            "cc": cc or [],
            "subject": subject,
            "body_plain": body_plain,
            "timestamp": "2026-10-13T10:00:00Z",
            "confirmed": True,
        }
        self.sent_messages.append(outbound)
        return {"status": "sent", "message_id": outbound["id"]}

    # Alias for API compatibility
    send_message = send

    def execute_action(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch action dynamically matching Skillware gmail_handler semantics."""
        act = action.strip().lower()
        if act == "search_messages":
            return {"messages": self.search_messages(parameters.get("query", []))}
        elif act == "read_message":
            return self.read_message(int(parameters.get("uid", 0)))
        elif act == "download_attachment":
            return self.download_attachment(
                uid=int(parameters.get("uid", 0)),
                part_index=int(parameters.get("part_index", 1)),
            )
        elif act == "preview_send":
            return self.preview_send(
                to=parameters.get("to", []),
                subject=parameters.get("subject", ""),
                body_plain=parameters.get("body_plain", ""),
                cc=parameters.get("cc"),
            )
        elif act == "send":
            return self.send(
                to=parameters.get("to", []),
                subject=parameters.get("subject", ""),
                body_plain=parameters.get("body_plain", ""),
                confirmed=bool(parameters.get("confirmed", False)),
                cc=parameters.get("cc"),
            )
        return {"status": "unknown_action", "action": action}

    def cleanup(self) -> None:
        """Tear down temporary mail directory."""
        if self._temp_dir_obj:
            self._temp_dir_obj.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
