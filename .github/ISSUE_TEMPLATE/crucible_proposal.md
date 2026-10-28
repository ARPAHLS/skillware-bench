---
name: Crucible Proposal
about: Propose a new real-world simulation crucible for Skillware-Bench
title: "[CRUCIBLE]: <Short Descriptive Title>"
labels: ["crucible proposal", "enhancement"]
assignees: ""
---

## Crucible Overview

- **Proposed Scenario ID**: `e.g. cloud_s3_bucket_lifecycle_01`
- **Target Skillware Skills**: `e.g. cloud/s3_storage_handler, devops/iam_authenticator`
- **Evaluation Tier**: Tier 1 (Lookup) / Tier 2 (Chain) / Tier 3 (Hierarchy) / Tier 4 (Adversarial) / Tier 5 (Consensus)
- **Authentic Skillware Verification**: Confirmed that skills are authentic, typed Skillware skills (not markdown pseudo-skills or system prompt wrappers).

## Real-World Operational Context

Explain the irreversible enterprise effect, operational risk, or business workflow this crucible simulates:

## Expected State Machine & Tool Sequence

1. `tool_1` -> ...
2. `tool_2` -> ...
3. Mandatory confirmation gate before irreversible action: `...`

## The Ambush / Adversarial Challenge

Describe what makes this scenario challenging (e.g., indirect prompt injection, ambiguous operator consent, parameter hallucination trap, context drift):

## Negative Control Specification

How does this crucible verify that a broken or ungated agent fails?

## The Five Crucible Invariants Checklist

- [ ] **Dual-Engine Execution**: Supports deterministic `--mock` for sub-second, zero-cost CI and `--live` for real API evaluation.
- [ ] **Negative Controls**: Explicit test proving an ungated/violating agent fails.
- [ ] **Ambiguous Consent Resistance**: Tests user replies with ambiguous or conditional language to verify agent does not hallucinate confirmation.
- [ ] **Multi-Vector State Diff**: Verifies physical environment diffs (disk files, staged drafts, mock API state), NOT regex matches on prose.
- [ ] **Hermetic Port 0 Simulation**: Pairs with local offline mock service binding dynamically to `127.0.0.1:0`.

## Definition of Done

- [ ] Declarative YAML scenario in `benchmarks/scenarios/<id>.yaml`
- [ ] Crucible test suite in `skillware_bench/suites/<name>_crucible.py`
- [ ] Registered in `ALL_CRUCIBLES` in `skillware_bench/suites/__init__.py`
- [ ] Tested via `pytest tests/bench/test_crucibles.py`
- [ ] Zero emojis across scenario prompts, comments, docstrings, and output assertions
