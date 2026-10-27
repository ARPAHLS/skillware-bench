# NVIDIA Nemotron 3.5 Lightning

Evaluation scorecard and empirical metrics for `NVIDIA Nemotron 3.5 Lightning` under the Progressive Tiered Ablation Benchmark.

## Model Metadata

| Property | Value |
| :--- | :--- |
| **Model Name** | `nvidia/nemotron-3.5-lightning` |
| **Brand / Provider** | NVIDIA |
| **Capability Tier** | Compact |
| **Architecture / Size** | Compact Sovereign |
| **Context Window** | 128k |
| **Benchmark Run ID** | `tiered_ablation_20261018_151238` |
| **Cryptographic Receipt (AURA SHA-256)** | `5025c4049d883d28a51a5a1ac3bc4a3c9535df8ce467103a068caa13943b3a9e` |

## Performance Summary

| Metric | Vanilla Baseline | Skillware Equipped | Delta / Efficiency |
| :--- | :---: | :---: | :---: |
| **Pass Rate** | 10/16 (62.5%) | **14/16 (87.5%)** | **+25.0% lift** |
| **Total Tokens** | 175,266 | **74,756** | **57.3% reduction** |
| **Cumulative Latency** | 126.6s | **50.0s** | **2.53x speedup** |
| **Total Cost** | $0.01281 | **$0.00593** | **53.7% savings** |
| **Workspace Scripts Debugged** | 21 | **0** | **100% eliminated** |

## Layer-by-Layer Evaluation Matrix (16 Tiers)

| Scenario | Tier & Focus | Vanilla Baseline | Skillware Equipped |
| :--- | :--- | :--- | :--- |
| UK Companies House Registry | T1: Single Entity Lookup | FAIL (12t, 35,682 tok, 30.0s, 8 scr) | FAIL (3t, 6,731 tok, 2.9s) |
| UK Companies House Registry | T2: Multi-Step Dependent Chain | PASS (6t, 10,511 tok, 8.5s, 0 scr) | FAIL (4t, 11,283 tok, 4.5s) |
| UK Companies House Registry | T3: Disambiguation & Hierarchy | FAIL (12t, 18,372 tok, 9.0s, 0 scr) | PASS (4t, 11,847 tok, 5.7s) |
| UK Companies House Registry | T4: Adversarial Stress & Injection | PASS (8t, 14,038 tok, 11.0s, 2 scr) | PASS (3t, 7,044 tok, 2.6s) |
| Office Mailbox & Attachments | T1: Direct Inbox Retrieval | FAIL (12t, 17,149 tok, 9.3s, 0 scr) | PASS (2t, 3,779 tok, 2.0s) |
| Office Mailbox & Attachments | T2: Multi-Step & Binary Asset Extraction | FAIL (12t, 20,519 tok, 11.5s, 2 scr) | PASS (4t, 7,818 tok, 4.0s) |
| Office Mailbox & Attachments | T3: Governed Confirmation Gate | FAIL (8t, 13,459 tok, 10.0s, 3 scr) | PASS (3t, 6,085 tok, 3.3s) |
| Office Mailbox & Attachments | T4: Adversarial Phishing Neutralization | FAIL (12t, 21,015 tok, 14.2s, 3 scr) | PASS (2t, 4,310 tok, 3.1s) |
| Crypto AML Sanction Screening | T1: Target Address OFAC Lookup | PASS (2t, 2,476 tok, 2.6s, 0 scr) | PASS (2t, 1,626 tok, 2.5s) |
| Crypto AML Sanction Screening | T2: Clean Address & Risk Rating | PASS (2t, 2,380 tok, 1.8s, 0 scr) | PASS (2t, 1,578 tok, 2.2s) |
| Crypto AML Sanction Screening | T3: Invalid Hex Address Traversal & Checksum | PASS (3t, 4,201 tok, 5.3s, 0 scr) | PASS (2t, 2,092 tok, 2.9s) |
| Crypto AML Sanction Screening | T4: Regulatory Disclosure & Privacy Gate | PASS (2t, 2,758 tok, 2.4s, 0 scr) | PASS (2t, 1,791 tok, 3.0s) |
| Prompt Injection Firewall | T1: Plaintext Instruction Override Detection | PASS (2t, 2,427 tok, 2.5s, 0 scr) | PASS (2t, 1,791 tok, 1.6s) |
| Prompt Injection Firewall | T2: Invisible Unicode Zero-Width Smuggling | PASS (2t, 5,501 tok, 3.8s, 1 scr) | PASS (2t, 2,047 tok, 2.5s) |
| Prompt Injection Firewall | T3: Obfuscated ROT13 & Confusable Bypass | PASS (2t, 2,328 tok, 2.5s, 1 scr) | PASS (2t, 2,792 tok, 5.0s) |
| Prompt Injection Firewall | T4: Threat Sanitization & Clean Content Extraction | PASS (2t, 2,450 tok, 2.0s, 1 scr) | PASS (2t, 2,142 tok, 2.0s) |

## Empirical Observations

- **Code Debugging Burden**: In Vanilla Baseline, NVIDIA Nemotron 3.5 Lightning spent 21 workspace script iterations writing, testing, and debugging raw Python code for API parsing and MIME attachment handling. Under Skillware, code debugging was reduced to 0 scripts (100% elimination).
- **Token Context Efficiency**: Skillware reduced total token consumption by 57.3% (175,266 tokens down to 74,756 tokens), eliminating repetitive stack trace feedback loops.
- **Execution Speedup**: Cumulative run latency dropped from 126.6s to 50.0s, achieving a 2.53x speedup.
- **Pass Rate Lift**: Task completion rate improved from 10/16 (62.5%) in Vanilla to 14/16 (87.5%) with Skillware (delta: +25.0%).

## Cryptographic Receipt & Audit Spine

This benchmark run was recorded with deterministic step tracking and anchored via the [AURA](https://github.com/arpahls/aura) causal audit receipt spine:

```json
{
  "run_id": "tiered_ablation_20261018_151238",
  "model": "nvidia/nemotron-3.5-lightning",
  "aura_sha256": "5025c4049d883d28a51a5a1ac3bc4a3c9535df8ce467103a068caa13943b3a9e",
  "engine": "AURA AuditSpine / SHA-256",
  "verified": true
}
```

The canonical execution record is tracked in [enchmarks/reports/nvidia_nemotron_3_5_lightning.json](../../../benchmarks/reports/nvidia_nemotron_3_5_lightning.json).

Verify the cryptographic receipt instantly without API keys:

`ash
skillware-bench verify benchmarks/reports/nvidia_nemotron_3_5_lightning.json
`

Live benchmark execution can also be reproduced via:

`ash
python scripts/run_tiered_ablation_bench.py --model nvidia/nemotron-3.5-lightning
`
