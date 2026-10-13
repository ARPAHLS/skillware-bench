# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Command Line Interface for Skillware-Bench."""

import argparse
import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from skillware_bench import __version__
from skillware_bench.core.runner import HarnessRunner
from skillware_bench.suites import ALL_CRUCIBLES

# Load local .env credentials automatically
load_dotenv()


def cmd_list(args, console: Console):
    """List all available crucibles and evaluation suites."""
    console.print(
        Panel(
            f"[bold cyan]Skillware-Bench[/bold cyan] v{__version__} - Crucible Catalog",
            expand=False,
        )
    )
    for key, crucible_cls in ALL_CRUCIBLES.items():
        scenario = crucible_cls.get_scenario()
        console.print(f"* [bold green]{key}[/bold green] ([dim]{scenario.id}[/dim])")
        console.print(f"  Title: {scenario.title}")
        console.print(f"  Tier:  {scenario.tier.value} | Category: {scenario.category}")
        console.print(f"  Skills: {', '.join(scenario.skills)}")
        console.print(f"  Prompt: [dim]{scenario.prompt}[/dim]\n")


def cmd_check_env(args, console: Console):
    """Inspect environment variables and API keys for live provider testing."""
    table = Table(title="Skillware-Bench Environment & Provider Key Verification")
    table.add_column("Provider / Secret", style="cyan")
    table.add_column("Env Var Name", style="magenta")
    table.add_column("Status", justify="center")
    table.add_column("Details", style="dim")

    keys_to_check = [
        ("OpenAI API", "OPENAI_API_KEY", "Required for GPT-4o, o3-mini, o1"),
        ("Anthropic API", "ANTHROPIC_API_KEY", "Required for Claude 3.7 Sonnet, Haiku"),
        ("Google Gemini API", "GEMINI_API_KEY", "Required for Gemini 2.5 Pro/Flash"),
        ("Google GenAI Alt", "GOOGLE_API_KEY", "Alternative key for Gemini SDK"),
        ("Mistral AI API", "MISTRAL_API_KEY", "Required for Mistral Large, Codestral"),
        ("Ollama Host", "OLLAMA_HOST", "Default: http://localhost:11434"),
        ("UK Companies House", "COMPANIES_HOUSE_API_KEY", "Required for live Companies House"),
        ("Etherscan API", "ETHERSCAN_API_KEY", "Required for live wallet screening"),
    ]

    for label, env_var, note in keys_to_check:
        val = os.environ.get(env_var)
        if val:
            masked = f"{val[:4]}...{val[-3:]}" if len(val) > 8 else "***"
            status = "[green]CONFIGURED[/green]"
            details = f"Value: {masked} ({note})"
        else:
            status = "[yellow]UNSET[/yellow]"
            details = note
        table.add_row(label, env_var, status, details)

    console.print(table)


def cmd_run(args, console: Console):
    """Run benchmark crucibles and print evaluation matrix."""
    runner = HarnessRunner(console=console)
    suite_label = args.suite or "all"
    is_mock = not args.live if args.live else args.mock

    mode_label = "MOCK (deterministic offline)" if is_mock else "LIVE (real API execution)"
    console.print(
        f"[bold]Running Skillware-Bench suite='{suite_label}' model='{args.model}' mode='{mode_label}'...[/bold]\n"
    )
    adapter_arg = getattr(args, "adapter", None)
    adapter_path = adapter_arg if isinstance(adapter_arg, str) and adapter_arg.strip() else None

    deltas = runner.run_suite(
        suite_name=args.suite,
        model_name=args.model,
        mock=is_mock,
        adapter_path=adapter_path,
    )
    runner.render_summary_table(deltas)

    if args.export:
        runner.export_reports(deltas, output_dir=args.output_dir)


def cmd_compare(args, console: Console):
    """Print detailed turn-by-turn comparison for a specific crucible."""
    if args.suite not in ALL_CRUCIBLES:
        console.print(
            f"[red]Error: Unknown suite '{args.suite}'. Use 'skillware-bench list' to see available suites.[/red]"
        )
        sys.exit(1)

    runner = HarnessRunner(console=console)
    deltas = runner.run_suite(suite_name=args.suite, model_name=args.model, mock=True)
    d = deltas[0]

    console.print(
        Panel(
            f"[bold cyan]Crucible Deep Dive: {d.scenario_id}[/bold cyan] ({d.model})", expand=False
        )
    )
    console.print("[bold yellow]1. Generic Baseline (Without Skillware):[/bold yellow]")
    b_score = d.baseline.score.composite_score
    console.print(
        f"   Latency: {d.baseline.latency_seconds:.1f}s | Tokens: {d.baseline.total_tokens} | Score: {b_score}/100"
    )
    if d.baseline.score.violations:
        console.print("   Violations:")
        for v in d.baseline.score.violations:
            console.print(f"     [red][X] {v}[/red]")
    console.print(f"   Sample Output: [dim]{d.baseline.trajectory[-1].raw_response}[/dim]\n")

    console.print("[bold green]2. Skillware Equipped:[/bold green]")
    s_lat = d.with_skillware.latency_seconds
    s_tok = d.with_skillware.total_tokens
    s_score = d.with_skillware.score.composite_score
    console.print(f"   Latency: {s_lat:.1f}s | Tokens: {s_tok} | Score: {s_score}/100")
    executed_actions = [tc.action for step in d.with_skillware.trajectory for tc in step.tool_calls]
    console.print(f"   Tool Actions Executed: {executed_actions}")
    console.print(f"   Sample Output: [dim]{d.with_skillware.trajectory[-1].raw_response}[/dim]\n")

    console.print("[bold cyan]3. Empirical Lift (Delta Matrix):[/bold cyan]")
    console.print(f"   * Latency Reduction: [yellow]-{d.latency_reduction_pct:.1f}%[/yellow]")
    console.print(f"   * Token Bloat Reduction: [cyan]-{d.token_reduction_pct:.1f}%[/cyan]")
    console.print(f"   * Composite Score Lift: [green]+{d.composite_score_lift:.1f} pts[/green]")


def cmd_verify(args, console: Console):
    """Verify cryptographic hash chain and Ed25519 signature of an AURA audit trace."""
    from skillware_bench.core.provenance import ProvenanceEngine

    trace_file = args.trace
    console.print(f"[bold]Verifying AURA audit trace: {trace_file}...[/bold]\n")
    try:
        res = ProvenanceEngine.verify_trace(trace_file)
        if res["valid"]:
            console.print(
                "[bold green][PASS] Cryptographic Trace Verification Succeeded[/bold green]"
            )
            console.print(f"  * Events Verified: {res['events_verified']}")
            console.print(f"  * Root Hash: [cyan]{res['root_hash']}[/cyan]")
            if res.get("signature_verified") is True:
                console.print("  * Ed25519 Signature: [green]AUTHENTIC[/green]")
            elif res.get("signature_verified") is False:
                console.print("  * Ed25519 Signature: [red]INVALID / TAMPERED[/red]")
            else:
                console.print(
                    "  * Ed25519 Signature: [yellow]UNSET (No .sig receipt found)[/yellow]"
                )
            console.print(f"  * Constitutional Approvals: {res['constitutional_approvals']}")
            console.print(f"  * Constitutional Violations: {res['constitutional_violations']}")
        else:
            console.print("[bold red][FAIL] Trace Verification Failed[/bold red]")
            console.print(f"  * Reason: Hash chain broken at event '{res.get('broken_event_id')}'")
            sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error verifying trace: {str(e)}[/bold red]")
        sys.exit(1)


def cmd_export_compliance(args, console: Console):
    """Export ISO/IEC 42001 and EU AI Act Article 14 regulatory oversight assessment."""
    from skillware_bench.core.provenance import ProvenanceEngine

    trace_file = args.trace
    output_file = args.output
    console.print(f"[bold]Generating Regulatory Compliance Package for {trace_file}...[/bold]\n")
    try:
        report = ProvenanceEngine.export_compliance_report(trace_file, output_path=output_file)
        table = Table(title="AI Regulatory Oversight Assessment (EU AI Act & ISO 42001)")
        table.add_column("Regulatory Standard", style="cyan")
        table.add_column("Compliance Status", justify="center")
        table.add_column("Audit Evidence / Proof", style="dim")

        for std_name, std_data in report["standards"].items():
            status_style = (
                "[green]COMPLIANT[/green]"
                if std_data["status"] == "COMPLIANT"
                else f"[yellow]{std_data['status']}[/yellow]"
            )
            table.add_row(std_name.replace("_", " "), status_style, std_data["evidence"])

        console.print(table)
        if output_file:
            console.print(f"\n[green]Saved full regulatory report to: {output_file}[/green]")
    except Exception as e:
        console.print(f"[bold red]Error generating compliance export: {str(e)}[/bold red]")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="skillware-bench",
        description="The transparent, empirical benchmark suite and evaluation harness for Skillware.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # list
    p_list = subparsers.add_parser("list", help="List available simulation crucibles and tiers")
    p_list.set_defaults(func=cmd_list)

    # check-env
    p_check = subparsers.add_parser(
        "check-env", help="Check configured environment variables and provider keys"
    )
    p_check.set_defaults(func=cmd_check_env)

    # run
    p_run = subparsers.add_parser("run", help="Run benchmark suite")
    p_run.add_argument(
        "--suite",
        choices=list(ALL_CRUCIBLES.keys()),
        default=None,
        help="Specific crucible suite to run",
    )
    p_run.add_argument("--model", default="golden-target", help="Model name identifier")
    p_run.add_argument(
        "--adapter",
        default=None,
        help="Path to custom model adapter Python file for BYOM evaluation",
    )
    p_run.add_argument(
        "--mock", action="store_true", default=True, help="Run offline mock crucibles"
    )

    p_run.add_argument(
        "--live",
        action="store_true",
        default=False,
        help="Run live model execution against crucibles",
    )
    p_run.add_argument(
        "--export", action="store_true", default=False, help="Export benchmark reports to JSON"
    )
    p_run.add_argument(
        "--output-dir", default="./runs/reports", help="Output directory for reports"
    )
    p_run.set_defaults(func=cmd_run)

    # compare
    p_cmp = subparsers.add_parser(
        "compare", help="Compare with-skillware vs without-skillware in depth"
    )
    p_cmp.add_argument(
        "--suite", required=True, choices=list(ALL_CRUCIBLES.keys()), help="Crucible to inspect"
    )
    p_cmp.add_argument("--model", default="golden-target", help="Model name identifier")
    p_cmp.set_defaults(func=cmd_compare)

    # verify
    p_verify = subparsers.add_parser(
        "verify", help="Cryptographically verify AURA causal audit traces and signatures"
    )
    p_verify.add_argument("trace", help="Path to .aura.jsonl audit trace file")
    p_verify.set_defaults(func=cmd_verify)

    # export-compliance
    p_comp = subparsers.add_parser(
        "export-compliance",
        help="Generate ISO 42001 and EU AI Act Article 14 compliance report",
    )
    p_comp.add_argument("trace", help="Path to .aura.jsonl audit trace file")
    p_comp.add_argument("--output", default=None, help="Optional output JSON filepath for report")
    p_comp.set_defaults(func=cmd_export_compliance)

    args = parser.parse_args()
    console = Console()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args, console)


if __name__ == "__main__":
    main()
