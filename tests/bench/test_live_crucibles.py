# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Unit tests for crucible run_live multi-turn execution and delta evaluation."""

import pytest
from skillware_bench.core.adapters.mock_adapter import MockModelAdapter
from skillware_bench.core.evaluators import CrucibleEvaluator
from skillware_bench.suites import ALL_CRUCIBLES


@pytest.mark.parametrize("crucible_key,crucible_cls", list(ALL_CRUCIBLES.items()))
def test_crucible_run_live_execution(crucible_key, crucible_cls):
    assert hasattr(crucible_cls, "run_live"), f"{crucible_key} must implement run_live"

    adapter = MockModelAdapter(model_name="mock-live-target")
    baseline, skillware = crucible_cls.run_live(model_name="mock-live-target", adapter=adapter)

    assert baseline.configuration == "generic_baseline"
    assert skillware.configuration == "skillware_equipped"
    assert baseline.scenario_id == skillware.scenario_id

    delta = CrucibleEvaluator.compute_delta(baseline, skillware)
    assert delta.model == "mock-live-target"
    assert isinstance(delta.composite_score_lift, float)
