# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Unit tests for Skillware-Bench simulation crucibles."""

import pytest
from skillware_bench.suites import ALL_CRUCIBLES
from skillware_bench.core.evaluators import CrucibleEvaluator


def test_all_crucibles_registered():
    assert len(ALL_CRUCIBLES) >= 7
    assert "gmail" in ALL_CRUCIBLES
    assert "companies_house" in ALL_CRUCIBLES
    assert "wallet_screening" in ALL_CRUCIBLES
    assert "constitution" in ALL_CRUCIBLES
    assert "chained_pipeline" in ALL_CRUCIBLES
    assert "prompt_injection" in ALL_CRUCIBLES
    assert "context_drift" in ALL_CRUCIBLES


@pytest.mark.parametrize("name,crucible_cls", ALL_CRUCIBLES.items())
def test_crucible_mock_execution(name, crucible_cls):
    scenario = crucible_cls.get_scenario()
    assert scenario.id is not None
    assert len(scenario.skills) > 0
    assert scenario.tier is not None

    baseline, skillware = crucible_cls.run_mock(model_name="test-model")
    assert baseline.model == "test-model"
    assert skillware.model == "test-model"
    assert baseline.configuration == "generic_baseline"
    assert skillware.configuration == "skillware_equipped"

    delta = CrucibleEvaluator.compute_delta(baseline, skillware)
    assert delta.token_reduction_pct > 0.0, f"Crucible {name} should exhibit token reduction"
    assert delta.composite_score_lift > 0.0, f"Crucible {name} should show positive score lift"
    assert skillware.score.passed is True, f"Skillware configuration must pass scenario {name}"
