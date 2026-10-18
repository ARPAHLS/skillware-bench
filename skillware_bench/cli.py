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
        ("OpenRouter API", "OPENROUTER_API", "Primary OpenRouter key for frontier/free models"),
        ("OpenRouter Alt", "OPENROUTER_API_KEY", "Alternative OpenRouter key variable"),
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

    if getattr(args, "figures", False):
        runner.export_figures(deltas, output_dir=getattr(args, "figures_dir", "./runs/figures"))


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
    except Exception as e:
        console.print(f"[bold red]Error generating compliance export: {str(e)}[/bold red]")
        sys.exit(1)


def cmd_dashboard(args, console: Console):
    """Generate self-contained interactive HTML dashboard from benchmark runs."""
    from pathlib import Path
    import webbrowser
    from skillware_bench.dashboard import DashboardGenerator

    runner = HarnessRunner(console=console)
    is_mock = not args.live
    console.print("[bold]Generating interactive Skillware-Bench dashboard...[/bold]\n")
    deltas = runner.run_suite(suite_name=args.suite, model_name=args.model, mock=is_mock)
    output_html = args.output or "./runs/dashboard.html"
    DashboardGenerator.generate_html(deltas, output_path=output_html)
    console.print(f"[bold green]Dashboard generated successfully:[/bold green] {output_html}")
    if getattr(args, "open_browser", False):
        webbrowser.open(str(Path(output_html).resolve().as_uri()))


def cmd_perturb(args, console: Console):
    """Generate dynamic anti-contamination scenario variations."""
    from skillware_bench.core.perturbations import PerturbationEngine

    engine = PerturbationEngine(seed=args.seed)
    console.print(
        Panel(
            "[bold cyan]Skillware-Bench Anti-Contamination Perturbation Engine[/bold cyan]",
            expand=False,
        )
    )

    suites = [args.suite] if args.suite else list(ALL_CRUCIBLES.keys())
    variants_table = Table(title="Generated Anti-Contamination Scenario Variants")
    variants_table.add_column("Crucible", style="cyan")
    variants_table.add_column("Variant ID", style="magenta")
    variants_table.add_column("Perturbed Prompt", style="dim")

    count = getattr(args, "count", 3)
    for s_name in suites:
        scenario = ALL_CRUCIBLES[s_name].get_scenario()
        for _ in range(count):
            perturbed = engine.perturb_scenario(scenario)
            preview = perturbed.prompt.replace("\n", " ")[:90] + "..."
            variants_table.add_row(s_name, perturbed.id, preview)

    console.print(variants_table)
    total_variants = len(suites) * count
    console.print(
        f"[dim]Generated {total_variants} variant(s) across {len(suites)} crucible(s). "
        "Invariants strictly preserved.[/dim]\n"
    )


def cmd_new_model(args, console: Console):
    """Scaffold a custom model adapter template for Bring-Your-Own-Model (BYOM) evaluation."""
    raw_name = args.name.lower().replace("-", "_").replace(" ", "_")
    output_path = args.output or f"./custom_adapters/{raw_name}_adapter.py"
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    class_name = "".join(part.title() for part in raw_name.split("_")) + "Adapter"

    template = f'''# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Custom Bring-Your-Own-Model adapter for {args.name}."""

from typing import Any, Dict, List, Optional
from skillware_bench.core.adapters.base import (
    BaseModelAdapter,
    ModelResponse,
    TokenUsage,
)
from skillware_bench.core.adapters.registry import AdapterRegistry


class {class_name}(BaseModelAdapter):
    """Adapter for {args.name}."""

    def __init__(self, model_name: str = "{args.name}", **kwargs):
        super().__init__(model_name=model_name, **kwargs)

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> ModelResponse:
        """Execute chat completion with tool calling."""
        # TODO: Implement inference call to your custom LLM or API endpoint
        return ModelResponse(
            content="Processed under constitutional governance.",
            tool_calls=[],
            usage=TokenUsage(prompt_tokens=100, completion_tokens=50),
        )


# Automatic BYOM Registration
AdapterRegistry.register("{args.name}", {class_name})
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(template)

    console.print(
        Panel(
            f"[bold green]Custom Model Adapter Scaffolded Successfully[/bold green]\n\n"
            f"File: [cyan]{output_path}[/cyan]\n\n"
            f"Run benchmark with:\n"
            f"[bold]skillware-bench run --adapter {output_path} --suite gmail[/bold]",
            expand=False,
        )
    )


def cmd_audit(args, console: Console):
    """Inspect and audit AURA causal provenance traces in detail."""
    from skillware_bench.core.provenance import ProvenanceEngine

    trace_file = args.trace
    console.print(f"[bold cyan]Auditing AURA Causal Provenance Trace: {trace_file}[/bold cyan]\n")
    try:
        res = ProvenanceEngine.verify_trace(trace_file)
        if not res["valid"]:
            console.print(
                f"[bold red][FAIL] Trace integrity invalid. Broken at event '{res.get('broken_event_id')}'.[/bold red]"
            )
            sys.exit(1)

        table = Table(title="Trace Audit Summary")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green bold")

        table.add_row("Events Verified", str(res["events_verified"]))
        table.add_row("Root Hash", res["root_hash"][:16] + "...")
        table.add_row("Constitutional Approvals", str(res["constitutional_approvals"]))
        table.add_row("Constitutional Violations", str(res["constitutional_violations"]))
        sig_val = "AUTHENTIC" if res.get("signature_verified") else "UNSET / NOT SIGNED"
        table.add_row("Ed25519 Signature", sig_val)

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error auditing trace: {str(e)}[/bold red]")
        sys.exit(1)


def cmd_menu(args, console: Console):
    """Launch interactive pastel dispatch menu."""
    banner_lines = [
        r"  ____  _     _ _ _                              ____                  _",
        r" / ___|| | __(_) | |_      ____ _ _ __ ___      | __ )  ___ _ __   ___| |__",
        r" \___ \| |/ /| | | \ \ /\ / / _` | '__/ _ \_____|  _ \ / _ \ '_ \ / __| '_ \\",
        r"  ___) |   < | | | |\ V  V / (_| | | |  __/_____| |_) |  __/ | | | (__| | | |",
        r" |____/|_|\_\|_|_|_| \_/\_/ \__,_|_|  \___|     |____/ \___|_| |_|\___|_| |_|",
    ]
    banner = "\n" + "\n".join(banner_lines)
    console.print(f"[bold #bae6fd]{banner}[/bold #bae6fd]")
    console.print(
        "[bold #efcefa]Skillware-Bench: The Governed Agent Evaluation Platform[/bold #efcefa]"
    )
    console.print(f"[dim]Version {__version__} | ARPA Hellenic Logical Systems[/dim]\n")

    menu_table = Table(show_header=False, box=None)
    menu_table.add_column("Key", style="bold #bbf7d0", width=5)
    menu_table.add_column("Command", style="bold cyan", width=16)
    menu_table.add_column("Description", style="dim")

    menu_table.add_row("[1]", "run", "Execute benchmark suite across frontier/sovereign models")
    menu_table.add_row("[2]", "live", "Launch real-world zero-mock simulation crucibles")
    menu_table.add_row("[3]", "compare", "Turn-by-turn with-vs-without Skillware A/B inspection")
    menu_table.add_row("[4]", "dashboard", "Launch interactive browser dashboard")
    menu_table.add_row("[5]", "audit", "Inspect AURA causal provenance traces and receipts")
    menu_table.add_row("[6]", "perturb", "Generate dynamic anti-contamination task variants")
    menu_table.add_row("[7]", "new-model", "Scaffold custom model adapter plugin")
    menu_table.add_row("[8]", "check-env", "Inspect provider API keys and secrets")
    menu_table.add_row("[9]", "openrouter", "Benchmark models via OpenRouter API")
    menu_table.add_row("[0]", "exit", "Exit Skillware-Bench launcher")

    console.print(menu_table)


def cmd_openrouter(args, console: Console):
    """Run OpenRouter benchmark sweep across frontier, sovereign, or free models."""
    from skillware_bench.core.openrouter_engine import OpenRouterBenchmarkEngine

    models = args.models or ["nvidia/nemotron-3.5-super-vl:free"]
    crucibles = [args.suite] if args.suite else args.crucibles
    engine = OpenRouterBenchmarkEngine(console=console)
    _ = engine.run_sweep(
        models=models,
        crucible_filter=crucibles,
        sweep_name=args.sweep_name or "openrouter_cli_sweep",
        output_dir=args.output_dir or "./runs/openrouter_sweeps",
    )


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
    p_run.add_argument(
        "--figures",
        action="store_true",
        default=False,
        help="Generate standalone SVG figures (radar and empirical lift delta)",
    )
    p_run.add_argument(
        "--figures-dir",
        default="./runs/figures",
        help="Output directory for generated figures",
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

    # dashboard
    p_dash = subparsers.add_parser(
        "dashboard", help="Generate self-contained interactive HTML dashboard"
    )
    p_dash.add_argument(
        "--suite",
        choices=list(ALL_CRUCIBLES.keys()),
        default=None,
        help="Specific crucible suite to benchmark",
    )
    p_dash.add_argument("--model", default="golden-target", help="Model name identifier")
    p_dash.add_argument(
        "--live",
        action="store_true",
        default=False,
        help="Run live model execution",
    )
    p_dash.add_argument(
        "--output",
        default="./runs/dashboard.html",
        help="Output HTML filepath for dashboard",
    )
    p_dash.add_argument(
        "--open-browser",
        action="store_true",
        default=False,
        help="Open generated dashboard in default browser",
    )
    p_dash.set_defaults(func=cmd_dashboard)

    # perturb
    p_perturb = subparsers.add_parser(
        "perturb", help="Generate dynamic anti-contamination scenario variations"
    )
    p_perturb.add_argument(
        "--suite",
        choices=list(ALL_CRUCIBLES.keys()),
        default=None,
        help="Specific crucible suite to perturb",
    )
    p_perturb.add_argument(
        "--count", type=int, default=3, help="Number of perturbation variants per scenario"
    )
    p_perturb.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    p_perturb.set_defaults(func=cmd_perturb)

    # new-model
    p_new = subparsers.add_parser(
        "new-model", help="Scaffold custom model adapter template for Bring-Your-Own-Model (BYOM)"
    )
    p_new.add_argument("name", help="Identifier name for custom model adapter (e.g. llama-custom)")
    p_new.add_argument(
        "--output", default=None, help="Output Python filepath for scaffolded adapter"
    )
    p_new.set_defaults(func=cmd_new_model)

    # audit
    p_audit = subparsers.add_parser("audit", help="Inspect and audit AURA causal provenance traces")
    p_audit.add_argument("trace", help="Path to .aura.jsonl audit trace file")
    p_audit.set_defaults(func=cmd_audit)

    # openrouter
    p_or = subparsers.add_parser(
        "openrouter", help="Benchmark frontier and sovereign models via OpenRouter API"
    )
    p_or.add_argument(
        "--models",
        nargs="+",
        default=["nvidia/nemotron-3.5-super-vl:free"],
        help="One or more model slugs to evaluate on OpenRouter",
    )
    p_or.add_argument(
        "--suite",
        choices=list(ALL_CRUCIBLES.keys()),
        default=None,
        help="Specific crucible suite to run",
    )
    p_or.add_argument(
        "--crucibles",
        nargs="+",
        default=None,
        help="List of crucibles to run (default: all 7)",
    )
    p_or.add_argument(
        "--sweep-name",
        default="openrouter_cli_sweep",
        help="Custom label for the sweep audit report",
    )
    p_or.add_argument(
        "--output-dir",
        default="./runs/openrouter_sweeps",
        help="Output directory for reports",
    )
    p_or.set_defaults(func=cmd_openrouter)

    # menu
    p_menu = subparsers.add_parser("menu", help="Launch interactive pastel dispatch launcher")
    p_menu.set_defaults(func=cmd_menu)

    args = parser.parse_args()
    console = Console()

    if not args.command:
        if sys.stdin.isatty():
            cmd_menu(args, console)
        else:
            parser.print_help()
        sys.exit(0)

    args.func(args, console)


if __name__ == "__main__":
    main()
