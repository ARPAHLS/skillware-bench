# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Hermetic lightweight mock server for offline UK Companies House and Mailbox evaluation."""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlparse

from skillware_bench.fixtures.mock_companies_registry import MOCK_COMPANIES_REGISTRY
from skillware_bench.fixtures.mock_inbox_registry import MOCK_INBOX_REGISTRY


class HermeticMockRequestHandler(BaseHTTPRequestHandler):
    """Handles REST requests for Companies House and Office Mailbox mock services."""

    def log_message(self, format: str, *args: Any) -> None:
        """Suppress default stderr HTTP request logging to keep benchmark output clean."""
        pass

    def _send_json(self, status_code: int, data: Any) -> None:
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

    def _send_bytes(self, status_code: int, content_bytes: bytes, mime_type: str) -> None:
        self.send_response(status_code)
        self.send_header("Content-Type", mime_type)
        self.send_header("Content-Length", str(len(content_bytes)))
        self.end_headers()
        self.wfile.write(content_bytes)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        query_params = parse_qs(parsed.query)

        # Record in audit log
        self.server.record_request("GET", self.path, dict(self.headers))

        # Health probe
        if path in ("", "/health"):
            self._send_json(200, {"status": "ok", "service": "hermetic_mock_api"})
            return

        # -------------------------------------------------------------
        # 1. Companies House Endpoints
        # -------------------------------------------------------------
        # GET /search/companies?q=...
        if path == "/search/companies":
            q = query_params.get("q", [""])[0].lower().strip()
            items = []
            for c_num, comp in MOCK_COMPANIES_REGISTRY.items():
                if q in comp["company_name"].lower() or q in c_num:
                    items.append({
                        "company_number": c_num,
                        "title": comp["company_name"],
                        "company_status": comp["company_status"],
                        "date_of_creation": comp["date_of_creation"],
                        "company_type": comp["type"],
                        "address": comp["registered_office_address"],
                    })
            self._send_json(200, {"total_results": len(items), "items": items})
            return

        # GET /company/{id}
        parts = path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "company":
            c_num = parts[1].zfill(8)
            comp = MOCK_COMPANIES_REGISTRY.get(c_num)
            if comp:
                self._send_json(200, {
                    "company_number": c_num,
                    "company_name": comp["company_name"],
                    "company_status": comp["company_status"],
                    "date_of_creation": comp["date_of_creation"],
                    "type": comp["type"],
                    "registered_office_address": comp["registered_office_address"],
                })
            else:
                self._send_json(404, {"error": "Company not found", "company_number": c_num})
            return

        # GET /company/{id}/officers
        if len(parts) == 3 and parts[0] == "company" and parts[2] == "officers":
            c_num = parts[1].zfill(8)
            comp = MOCK_COMPANIES_REGISTRY.get(c_num)
            if comp:
                active_only = query_params.get("active_only", ["false"])[0].lower() == "true"
                role_filter = query_params.get("officer_role", [None])[0]
                officers = comp.get("officers", [])
                if active_only:
                    officers = [o for o in officers if "resigned_on" not in o]
                if role_filter:
                    officers = [o for o in officers if o.get("officer_role", "").lower() == role_filter.lower()]
                self._send_json(200, {
                    "total_results": len(officers),
                    "active_count": sum(1 for o in comp.get("officers", []) if "resigned_on" not in o),
                    "items": officers,
                })
            else:
                self._send_json(404, {"error": "Company not found", "company_number": c_num})
            return

        # GET /company/{id}/filing-history
        if len(parts) == 3 and parts[0] == "company" and parts[2] == "filing-history":
            c_num = parts[1].zfill(8)
            comp = MOCK_COMPANIES_REGISTRY.get(c_num)
            if comp:
                self._send_json(200, {
                    "total_results": len(comp.get("filings", [])),
                    "items": comp.get("filings", []),
                })
            else:
                self._send_json(404, {"error": "Company not found", "company_number": c_num})
            return

        # -------------------------------------------------------------
        # 2. Office Mailbox Endpoints
        # -------------------------------------------------------------
        # GET /email/search?q=...
        if path == "/email/search":
            q_terms = [t.lower() for t in query_params.get("q", [""])[0].split() if t]
            results = []
            for uid, msg in MOCK_INBOX_REGISTRY.items():
                haystack = f"{msg['from']} {msg['subject']} {msg['body_plain']}".lower()
                if not q_terms or all(t in haystack for t in q_terms):
                    results.append({
                        "uid": uid,
                        "from": msg["from"],
                        "subject": msg["subject"],
                        "date": msg["date"],
                        "has_attachments": len(msg.get("attachments", [])) > 0,
                    })
            self._send_json(200, {"messages": results})
            return

        # GET /email/{uid}
        if len(parts) == 2 and parts[0] == "email" and parts[1].isdigit():
            uid = int(parts[1])
            msg = MOCK_INBOX_REGISTRY.get(uid)
            if msg:
                # Do not leak raw bytes directly in message metadata envelope
                clean_msg = dict(msg)
                clean_atts = []
                for att in msg.get("attachments", []):
                    clean_atts.append({
                        "part_index": att.get("part_index", 1),
                        "filename": att.get("filename"),
                        "mime_type": att.get("mime_type"),
                        "size_bytes": len(att.get("content_bytes", b"")),
                    })
                clean_msg["attachments"] = clean_atts
                self._send_json(200, {"status": "success", "message": clean_msg})
            else:
                self._send_json(404, {"status": "error", "error": f"Message with UID {uid} not found"})
            return

        # GET /email/{uid}/attachment?part=1
        if len(parts) == 3 and parts[0] == "email" and parts[1].isdigit() and parts[2] == "attachment":
            uid = int(parts[1])
            part_idx = int(query_params.get("part", [1])[0])
            msg = MOCK_INBOX_REGISTRY.get(uid)
            if msg:
                for att in msg.get("attachments", []):
                    if att.get("part_index") == part_idx:
                        self.server.record_download(uid, att["filename"])
                        self._send_bytes(200, att["content_bytes"], att.get("mime_type", "application/octet-stream"))
                        return
                self._send_json(404, {"error": f"Attachment part {part_idx} not found on message {uid}"})
            else:
                self._send_json(404, {"error": f"Message {uid} not found"})
            return

        # -------------------------------------------------------------
        # 3. Crypto Wallet Screening Endpoints
        # -------------------------------------------------------------
        # GET /crypto/screen?address=...
        if path == "/crypto/screen":
            addr = query_params.get("address", [""])[0].strip()
            from skillware_bench.infra.wallet_screening_live import WalletScreeningClient
            client = WalletScreeningClient(api_key="mock")
            self._send_json(200, client.screen_address(addr))
            return

        self._send_json(404, {"error": f"Endpoint not found: {path}"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        content_len = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_len) if content_len > 0 else b"{}"

        try:
            body_json = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
        except Exception:
            body_json = {}

        self.server.record_request("POST", self.path, dict(self.headers), body_json)

        # POST /email/preview
        if path == "/email/preview":
            preview = {
                "status": "preview_ready",
                "to": body_json.get("to", []),
                "cc": body_json.get("cc", []),
                "subject": body_json.get("subject", ""),
                "body_plain": body_json.get("body_plain") or body_json.get("body", ""),
                "requires_confirmation": True,
                "agent_hint": "Display draft to operator and request confirmation before sending.",
            }
            self.server.staged_previews.append(preview)
            self._send_json(200, preview)
            return

        # POST /email/send (Strictly gated on confirmed=True)
        if path == "/email/send":
            confirmed = bool(body_json.get("confirmed", False))
            if not confirmed:
                self._send_json(403, {
                    "status": "gated",
                    "error": "Confirmation required before send. Call /email/preview first and verify human consent.",
                    "confirmed": False,
                })
                return

            outbound = {
                "id": len(self.server.sent_messages) + 1,
                "to": body_json.get("to", []),
                "cc": body_json.get("cc", []),
                "subject": body_json.get("subject", ""),
                "body_plain": body_json.get("body_plain") or body_json.get("body", ""),
                "confirmed": True,
            }
            self.server.sent_messages.append(outbound)
            self._send_json(200, {"status": "sent", "message_id": outbound["id"]})
            return

        # POST /security/scan (Prompt injection & text sanitization)
        if path == "/security/scan":
            text = body_json.get("source_text") or body_json.get("text", "")
            try:
                from skillware.core.loader import SkillLoader
                bundle = SkillLoader.load_skill("security/prompt_injection_firewall", check_requirements=False)
                cls = SkillLoader.get_skill_class(bundle)
                inst = cls()
                res = inst.execute({"source_text": text})
                self._send_json(200, res)
            except Exception as exc:
                self._send_json(500, {"error": str(exc)})
            return

        self._send_json(404, {"error": f"Endpoint not found: {path}"})


class HermeticMockServer(ThreadingHTTPServer):
    """Self-contained, thread-safe mock HTTP server on Port 0."""

    def __init__(self, host: str = "127.0.0.1", port: int = 0):
        super().__init__((host, port), HermeticMockRequestHandler)
        self.host = host
        self.port = self.server_port
        self.request_history: List[Dict[str, Any]] = []
        self.downloaded_attachments: List[Dict[str, Any]] = []
        self.staged_previews: List[Dict[str, Any]] = []
        self.sent_messages: List[Dict[str, Any]] = []
        self._thread: Optional[threading.Thread] = None

    def record_request(
        self, method: str, path: str, headers: Dict[str, str], body: Optional[Any] = None
    ) -> None:
        self.request_history.append({
            "method": method,
            "path": path,
            "headers": headers,
            "body": body,
        })

    def record_download(self, uid: int, filename: str) -> None:
        self.downloaded_attachments.append({"uid": uid, "filename": filename})

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def start(self) -> "HermeticMockServer":
        """Start server in background daemon thread."""
        self._thread = threading.Thread(target=self.serve_forever, daemon=True)
        self._thread.start()
        return self

    def stop(self) -> None:
        """Shutdown and close server."""
        self.shutdown()
        self.server_close()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

    def __enter__(self) -> "HermeticMockServer":
        return self.start()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.stop()
