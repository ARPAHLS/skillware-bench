---
name: Benchmark Report Submission
about: Submit an empirical 16-layer benchmark execution report for official publication
title: "[REPORT]: <Provider / Model Name> (v0.3.1)"
labels: ["benchmark report", "evaluation"]
assignees: ""
---

## Model Evaluation Details

- **Model Identifier**: `e.g. meta-llama/llama-4-maverick`
- **Provider / Host**: `e.g. Meta / Local vLLM / OpenRouter`
- **Capability Tier**: `Frontier` / `Enterprise` / `Compact` / `Edge`
- **Model Weights**: Open-Weight / Closed Commercial API

## Empirical Summary (16-Layer Progressive Matrix)

| Metric | Vanilla Baseline | Skillware Equipped | Delta / Efficiency |
| :--- | :--- | :--- | :--- |
| **Pass Rate** | `X / 16 (Y%)` | `Z / 16 (W%)` | `+N.N%` |
| **Total Tokens** | `N tokens` | `M tokens` | `-P.P%` |
| **Execution Latency** | `N.N s` | `M.M s` | `X.Xx speedup` |
| **Scripts Debugged** | `N attempts` | `0 attempts` | `-100%` |

## AURA Cryptographic Attestation

- **Run ID**: `tiered_ablation_YYYYMMDD_HHMMSS`
- **AURA Cryptographic Receipt (SHA-256)**: `<64-char SHA-256 digest>`
- **Attestation Engine**: `AURA AuditSpine / SHA-256`

## Local Verification Command

Run and paste the terminal output of the CLI verification check:

```bash
skillware-bench verify benchmarks/reports/<model_filename>.json
```

Output:
```text
<Paste output here>
```

## Submission Checklist

- [ ] Canonical report JSON placed in `benchmarks/reports/<model_filename>.json`
- [ ] Added model entry to `benchmarks/reports/README.md` master index table
- [ ] Created or updated model card in `docs/results/models/<model_filename>.md`
- [ ] Updated `docs/leaderboard.md` standings table
- [ ] Zero emojis across all committed files and documentation
