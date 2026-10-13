# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Unit tests for perturbation engine, statistical variance calculations, and SVG figure generators."""

from pathlib import Path
from skillware_bench.core.models import (
    ComparativeDeltaReport,
    CrucibleRunReport,
    CrucibleScore,
)
from skillware_bench.core.perturbations import PerturbationEngine
from skillware_bench.core.statistics import (
    MetricDistribution,
    StatisticalEvaluator,
    pass_at_k,
)
from skillware_bench.suites import ALL_CRUCIBLES
from skillware_bench.viz import VisualGenerator


def test_perturbation_engine_generates_variants():
    engine = PerturbationEngine(seed=42)
    scenario = ALL_CRUCIBLES["gmail"].get_scenario()
    perturbed = engine.perturb_scenario(scenario)

    assert perturbed.id != scenario.id
    assert "perturbed" in perturbed.id
    assert perturbed.category == scenario.category
    assert perturbed.tier == scenario.tier
    assert perturbed.expectations == scenario.expectations


def test_pass_at_k_statistical_calculations():
    # 5 runs, 5 passed, k=1 -> 1.0
    assert pass_at_k(5, 5, 1) == 1.0

    # 5 runs, 0 passed, k=1 -> 0.0
    assert pass_at_k(5, 0, 1) == 0.0

    # 10 runs, 7 passed, k=5 -> should be > 0.95
    p5 = pass_at_k(10, 7, 5)
    assert 0.95 <= p5 <= 1.0


def test_metric_distribution_calculations():
    samples = [10.0, 12.0, 14.0, 11.0, 13.0]
    dist = MetricDistribution.from_samples(samples)

    assert dist.mean == 12.0
    assert dist.min == 10.0
    assert dist.max == 14.0
    assert dist.std_dev > 0.0
    assert len(dist.confidence_interval_95) == 2


def test_statistical_evaluator_aggregation():
    stats = StatisticalEvaluator.aggregate_runs(
        scenario_id="office_gmail_01",
        model="gpt-4o",
        run_scores=[95.0, 90.0, 100.0, 85.0, 95.0],
        run_latencies=[1.2, 1.4, 1.1, 1.3, 1.2],
        run_tokens=[450, 480, 420, 460, 440],
        k=5,
    )

    assert stats.repetitions == 5
    assert stats.pass_at_1 == 1.0
    assert stats.pass_at_k == 1.0
    assert stats.scores.mean == 93.0
    assert stats.latencies.mean == 1.24
    assert stats.tokens.mean == 450.0


def test_visual_generator_radar_chart(tmp_path: Path):
    pillar_scores = {
        "Constitutional Pass": 100.0,
        "Adversarial Security": 95.0,
        "Sequence Compliance": 100.0,
        "Schema Fidelity": 98.0,
        "Error Recovery": 90.0,
        "Long-Horizon Retention": 100.0,
        "Ambiguous Consent": 100.0,
        "Disclaimer Freedom": 95.0,
        "Actionability": 95.0,
        "Economic Efficiency": 88.0,
    }

    out_svg = tmp_path / "radar.svg"
    svg_content = VisualGenerator.generate_radar_chart(pillar_scores, output_path=out_svg)

    assert "<svg" in svg_content
    assert "</svg>" in svg_content
    assert "Constitutional Pass" in svg_content
    assert out_svg.exists()


def test_visual_generator_delta_lift_chart(tmp_path: Path):
    dummy_report = CrucibleRunReport(
        scenario_id="office_gmail_01",
        model="golden-target",
        configuration="dummy",
        latency_seconds=1.0,
        total_tokens=100,
        word_count=20,
        score=CrucibleScore(),
    )
    deltas = [
        ComparativeDeltaReport(
            scenario_id="office_gmail_01",
            model="golden-target",
            baseline=dummy_report,
            with_skillware=dummy_report,
            latency_reduction_pct=62.5,
            token_reduction_pct=64.2,
            composite_score_lift=27.0,
        )
    ]

    out_svg = tmp_path / "delta.svg"
    svg_content = VisualGenerator.generate_delta_lift_chart(deltas, output_path=out_svg)

    assert "<svg" in svg_content
    assert "-64%" in svg_content
    assert "-62%" in svg_content
    assert out_svg.exists()


def test_dashboard_generator(tmp_path: Path):
    from skillware_bench.dashboard import DashboardGenerator

    dummy_report = CrucibleRunReport(
        scenario_id="office_gmail_01",
        model="golden-target",
        configuration="dummy",
        latency_seconds=1.0,
        total_tokens=100,
        word_count=20,
        score=CrucibleScore(),
    )
    deltas = [
        ComparativeDeltaReport(
            scenario_id="office_gmail_01",
            model="golden-target",
            baseline=dummy_report,
            with_skillware=dummy_report,
            latency_reduction_pct=62.5,
            token_reduction_pct=64.2,
            composite_score_lift=27.0,
        )
    ]

    out_html = tmp_path / "dashboard.html"
    html_content = DashboardGenerator.generate_html(deltas, output_path=out_html)

    assert "<!DOCTYPE html>" in html_content
    assert "Empirical Audit Dashboard" in html_content
    assert "office_gmail_01" in html_content
    assert out_html.exists()
