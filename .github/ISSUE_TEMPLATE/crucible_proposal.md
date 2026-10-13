---
name: Crucible Proposal
about: Propose a new real-world simulation crucible for Skillware-Bench
title: "[CRUCIBLE]: <Short Descriptive Title>"
labels: ["crucible proposal", "enhancement"]
assignees: ""
---

## Crucible Overview

- **Proposed Scenario ID**: `e.g. cloud_s3_bucket_lifecycle_01`
- **Target Skills**: `e.g. cloud/s3_storage_handler, devops/iam_authenticator`
- **Evaluation Tier**: Tier 3 (Constitutional Safety) / Tier 4 (Multi-Skill Pipeline) / Tier 5 (Economics)

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

## Definition of Done

- [ ] Declarative YAML scenario in `benchmarks/scenarios/<id>.yaml`
- [ ] Crucible test suite in `skillware_bench/suites/<name>_crucible.py`
- [ ] Registered in `skillware_bench/suites/__init__.py`
- [ ] Supports `--mock` for fast CI and `--live` for real API runs
- [ ] Zero emojis across scenario prompts, comments, and output assertions
