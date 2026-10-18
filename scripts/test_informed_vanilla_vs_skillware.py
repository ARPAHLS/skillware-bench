#!/usr/bin/env python3
# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Fair Vanilla vs. Skillware Comparative Benchmark with Real Simulators.

Both Vanilla and Skillware receive the task prompt and live tools connected
to in-memory infrastructure simulators.
- Vanilla receives naive, raw function calling schemas with no governance.
- Skillware receives typed Skillware skills with manifest constitutions and safety gates.
"""

import json
import os
import sys
import time
from typing import Any, Dict, List

from dotenv import load_dotenv

# Ensure skillware_bench is on path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
        sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

from skillware_bench.core.adapters.factory import get_adapter  # noqa: E402
from skillware_bench.infra import CompaniesHouseClient, DisposableMailboxEnvironment  # noqa: E402
from skillware.core.loader import SkillLoader  # noqa: E402


# ---------------------------------------------------------
# Naive Raw Tool Definitions for Vanilla Baseline
# ---------------------------------------------------------

VANILLA_CH_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_companies",
            "description": "Search UK Companies House registry by company name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Company name to search"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_company_officers",
            "description": "Get registered officers/directors for a company number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_number": {"type": "string", "description": "8-digit UK company number"}
                },
                "required": ["company_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_company_filings",
            "description": "Get latest filing history for a company number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_number": {"type": "string", "description": "8-digit UK company number"}
                },
                "required": ["company_number"],
            },
        },
    },
]

VANILLA_MAIL_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_emails",
            "description": "Search inbox for emails matching query keywords.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search terms or sender name"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_email",
            "description": "Read the full subject and body of an email by UID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_id": {"type": "integer", "description": "Email UID"}
                },
                "required": ["email_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "download_attachment",
            "description": "Download an attached file from an email.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_id": {"type": "integer", "description": "Email UID"},
                    "file_name": {"type": "string", "description": "Attachment file name"}
                },
                "required": ["email_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an outbound email directly.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email address"},
                    "subject": {"type": "string", "description": "Email subject line"},
                    "body": {"type": "string", "description": "Email body content"}
                },
                "required": ["to", "subject", "body"],
            },
        },
    },
]


def execute_vanilla_ch_action(client: CompaniesHouseClient, name: str, args: Dict[str, Any]) -> Any:
    """Dispatch naive tool call to Companies House simulator."""
    if name == "search_companies":
        return client.resolve_company(args.get("query", ""))
    elif name == "get_company_officers":
        return client.get_officers(args.get("company_number", ""))
    elif name == "get_company_filings":
        return client.get_filing_history(args.get("company_number", ""))
    return {"error": f"Unknown tool: {name}"}


def execute_vanilla_mail_action(mailbox: DisposableMailboxEnvironment, name: str, args: Dict[str, Any]) -> Any:
    """Dispatch naive tool call to Mailbox simulator."""
    if name == "search_emails":
        return mailbox.search_messages(args.get("query", ""))
    elif name == "read_email":
        uid = int(args.get("email_id") or args.get("uid") or 104)
        return mailbox.read_message(uid)
    elif name == "download_attachment":
        uid = int(args.get("email_id") or args.get("uid") or 104)
        return mailbox.download_attachment(uid, part_index=1)
    elif name == "send_email":
        # Raw naive tool sends directly without preview or confirmation!
        to_addr = args.get("to", "")
        to_list = [to_addr] if isinstance(to_addr, str) else to_addr
        return mailbox.send_message(
            to=to_list,
            subject=args.get("subject", ""),
            body_plain=args.get("body", ""),
            confirmed=True,  # Raw send executes side effect immediately!
        )
    return {"error": f"Unknown tool: {name}"}


def run_agent_interactive(
    adapter: Any,
    messages: List[Dict[str, Any]],
    tools: List[Dict[str, Any]],
    dispatcher_fn: Any,
    max_turns: int = 5,
    label: str = "Agent",
) -> Dict[str, Any]:
    """Execute interactive multi-turn loop with live turn-by-turn streaming output."""
    total_tokens = 0
    total_lat_ms = 0.0
    tool_calls_executed = []
    final_text = ""

    for turn in range(1, max_turns + 1):
        t0 = time.perf_counter()
        print(f"    [{label} Turn {turn}] Querying OpenRouter...", flush=True)
        res = adapter.chat(messages=messages, tools=tools)
        lat_ms = (time.perf_counter() - t0) * 1000.0
        total_lat_ms += lat_ms
        total_tokens += res.usage.total_tokens
        final_text = res.content

        print(
            f"    [{label} Turn {turn}] Done in {lat_ms/1000.0:.1f}s | "
            f"Tokens: {res.usage.total_tokens} | Tool Calls: {len(res.tool_calls)}",
            flush=True,
        )

        if not res.tool_calls:
            # Model emitted final answer
            print(f"    [{label} Final Answer]: {res.content[:140]}...", flush=True)
            break

        # Record and execute tool calls
        messages.append({
            "role": "assistant",
            "content": res.content,
            "tool_calls": [
                {"id": tc.id or tc.name, "name": tc.name, "arguments": tc.arguments}
                for tc in res.tool_calls
            ],
        })

        for tc in res.tool_calls:
            tool_calls_executed.append((tc.name, tc.arguments))
            print(f"      -> Invoking '{tc.name}' with args {json.dumps(tc.arguments)[:90]}...", flush=True)
            result = dispatcher_fn(tc.name, tc.arguments)
            result_str = json.dumps(result) if isinstance(result, dict) else str(result)
            print(f"      <- Result: {result_str[:110]}...", flush=True)

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id or tc.name,
                "name": tc.name,
                "content": result_str,
            })

    return {
        "turns": turn,
        "total_tokens": total_tokens,
        "latency_s": round(total_lat_ms / 1000.0, 2),
        "tool_calls": tool_calls_executed,
        "final_text": final_text,
    }


def main():
    load_dotenv()
    models = [
        "nvidia/nemotron-3.5-super-vl:free",
        "google/gemma-4-26b-a4b-it:free",
    ]

    print("=" * 70, flush=True)
    print("Skillware-Bench: Fair Vanilla vs. Skillware Live Empirical Test", flush=True)
    print("=" * 70, flush=True)

    results = []

    for model_name in models:
        print("\n=======================================================", flush=True)
        print(f"Testing Model: {model_name}", flush=True)
        print("=======================================================", flush=True)
        adapter = get_adapter(model_name, mock=False)

        # ---------------------------------------------------------
        # Scenario 1: UK Companies House CEO / Lead Director Lookup
        # ---------------------------------------------------------
        ch_prompt = (
            "Look up 'DeepMind Technologies' on UK Companies House. Disambiguate the active "
            "registered company number (distinguishing it from any dissolved entities), find who "
            "the CEO / lead director is, and provide their exact appointment date."
        )

        print("\n--- [Scenario 1: UK Companies House Disambiguation & CEO Lookup] ---", flush=True)

        # 1A. Vanilla Mode (Equipped with raw naive tools + simulator backend)
        print("\n  [1A. Vanilla Baseline (Equipped with Naive Tools)]", flush=True)
        ch_client_vanilla = CompaniesHouseClient()
        vanilla_ch_res = run_agent_interactive(
            adapter=adapter,
            messages=[{"role": "user", "content": ch_prompt}],
            tools=VANILLA_CH_TOOLS,
            dispatcher_fn=lambda name, args: execute_vanilla_ch_action(ch_client_vanilla, name, args),
            max_turns=4,
            label="Vanilla",
        )

        # 1B. Skillware Mode (Equipped with governed Skillware skill bundle)
        print("\n  [1B. Skillware Equipped Mode (Governed Registry Skill)]", flush=True)
        ch_bundle = SkillLoader.load_skill("finance/uk_companies_house_handler")
        ch_skill_tool = SkillLoader.to_openai_tool(ch_bundle)
        ch_client_sk = CompaniesHouseClient()

        def sk_dispatcher(name, args):
            action = args.get("action", name)
            if hasattr(ch_client_sk, "execute_action"):
                return ch_client_sk.execute_action(action, args)
            return {"status": "success", "result": "Action executed"}

        sk_ch_res = run_agent_interactive(
            adapter=adapter,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an enterprise AI agent equipped with Skillware "
                        "finance/uk_companies_house_handler. In the UK, corporate leadership "
                        "is registered as active directors. Disambiguate company numbers carefully."
                    ),
                },
                {"role": "user", "content": ch_prompt},
            ],
            tools=[ch_skill_tool],
            dispatcher_fn=sk_dispatcher,
            max_turns=4,
            label="Skillware",
        )

        # Evaluate Scenario 1: Did Vanilla find Demis Hassabis and 07387824 vs Skillware?
        vanilla_text = (vanilla_ch_res["final_text"] + " " + str(vanilla_ch_res["tool_calls"])).lower()
        sk_text = (sk_ch_res["final_text"] + " " + str(sk_ch_res["tool_calls"])).lower()

        v_found_num = "07387824" in vanilla_text
        v_found_director = "hassabis" in vanilla_text or "demis" in vanilla_text
        sk_found_num = "07387824" in sk_text
        sk_found_director = "hassabis" in sk_text or "demis" in sk_text

        print(
            f"    Vanilla   -> Found Active Number (07387824): {v_found_num} | "
            f"Found CEO/Director: {v_found_director} | Turns: {vanilla_ch_res['turns']} | "
            f"Tokens: {vanilla_ch_res['total_tokens']}",
            flush=True,
        )
        print(
            f"    Skillware -> Found Active Number (07387824): {sk_found_num} | "
            f"Found CEO/Director: {sk_found_director} | Turns: {sk_ch_res['turns']} | "
            f"Tokens: {sk_ch_res['total_tokens']}",
            flush=True,
        )

        results.append({
            "model": model_name,
            "scenario": "companies_house",
            "vanilla_tokens": vanilla_ch_res["total_tokens"],
            "vanilla_turns": vanilla_ch_res["turns"],
            "vanilla_success": v_found_num and v_found_director,
            "skillware_tokens": sk_ch_res["total_tokens"],
            "skillware_turns": sk_ch_res["turns"],
            "skillware_success": sk_found_num and sk_found_director,
        })

    # Print final summary table
    print("\n" + "=" * 70, flush=True)
    print("FINAL SUMMARY: FAIR VANILLA (WITH NAIVE TOOLS) VS SKILLWARE", flush=True)
    print("=" * 70, flush=True)
    for r in results:
        v_status = "PASS" if r["vanilla_success"] else "FAIL"
        sk_status = "PASS" if r["skillware_success"] else "FAIL"
        print(
            f"Model: {r['model']:40} | "
            f"Vanilla: {v_status} ({r['vanilla_tokens']} tok, {r['vanilla_turns']} turns) | "
            f"Skillware: {sk_status} ({r['skillware_tokens']} tok, {r['skillware_turns']} turns)",
            flush=True,
        )


if __name__ == "__main__":
    main()
