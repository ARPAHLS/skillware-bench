# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Harness runner executing crucibles, compiling reports, and rendering summaries."""

import json
import os
from typing import List, Optional
from rich.console import Console
from rich.table import Table

from skillware_bench.core.adapters import get_adapter
from skillware_bench.core.agent_loop import AgentLoop
from skillware_bench.core.evaluators import CrucibleEvaluator
from skillware_bench.core.models import ComparativeDeltaReport
from skillware_bench.suites import ALL_CRUCIBLES


class HarnessRunner:
    """Orchestrates benchmark crucible executions across suites."""

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()

    def run_suite(
        self,
        suite_name: Optional[str] = None,
        model_name: str = "golden-target",
        mock: bool = True,
    ) -> List[ComparativeDeltaReport]:
        reports: List[ComparativeDeltaReport] = []

        crucible_keys = (
            [suite_name]
            if suite_name and suite_name in ALL_CRUCIBLES
            else list(ALL_CRUCIBLES.keys())
        )

        adapter = get_adapter(model_name=model_name, mock=mock)

        for key in crucible_keys:
            crucible_cls = ALL_CRUCIBLES[key]
            if mock:
                baseline, skillware = crucible_cls.run_mock(model_name=model_name)
            else:
                scenario = crucible_cls.get_scenario()
                # 1. Baseline Run: model without Skillware tools
                baseline_loop = AgentLoop(
                    adapter=adapter,
                    skill_names=[],
                    system_prompt="You are a helpful assistant.",
                    mock=mock,
                )
                baseline = baseline_loop.run(
                    prompt=scenario.prompt,
                    scenario=scenario,
                    expectations=scenario.expectations,
                )
                baseline.configuration = "generic_baseline"

                # 2. Skillware Equipped Run: model with Skillware tools
                skillware_loop = AgentLoop(
                    adapter=adapter,
                    skill_names=scenario.skills,
                    mock=mock,
                )
                skillware = skillware_loop.run(
                    prompt=scenario.prompt,
                    scenario=scenario,
                    expectations=scenario.expectations,
                )
                skillware.configuration = "skillware_equipped"

            delta = CrucibleEvaluator.compute_delta(baseline, skillware)
            reports.append(delta)

        return reports

    def render_summary_table(self, deltas: List[ComparativeDeltaReport]):
        table = Table(
            title="Skillware-Bench Empirical Progression & Delta Matrix", show_header=True
        )
        table.add_column("Crucible / Suite", style="cyan", no_wrap=True)
        table.add_column("Model", style="magenta")
        table.add_column("Base Score", justify="right")
        table.add_column("Skillware Score", justify="right", style="green bold")
        table.add_column("Score Lift", justify="right", style="bold")
        table.add_column("Latency Drop", justify="right", style="yellow")
        table.add_column("Token Drop", justify="right", style="cyan")
        table.add_column("Pass", justify="center")

        for d in deltas:
            pass_status = (
                "[green]PASS[/green]" if d.with_skillware.score.passed else "[red]FAIL[/red]"
            )
            lift_style = "[green]+" if d.composite_score_lift > 0 else "[red]"
            table.add_row(
                d.scenario_id,
                d.model,
                f"{d.baseline.score.composite_score:.1f}",
                f"{d.with_skillware.score.composite_score:.1f}",
                f"{lift_style}{d.composite_score_lift:.1f}[/]",
                f"-{d.latency_reduction_pct:.1f}%",
                f"-{d.token_reduction_pct:.1f}%",
                pass_status,
            )

        self.console.print(table)

    def export_reports(
        self, deltas: List[ComparativeDeltaReport], output_dir: str = "./runs/reports"
    ):
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "benchmark_report.json")
        payload = [d.model_dump() for d in deltas]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        self.console.print(f"[dim]Exported benchmark report to [bold]{path}[/bold][/dim]")
