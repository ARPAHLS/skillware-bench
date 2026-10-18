# Thematic Analysis: Token Economics & Overhead Work Avoided

## Overview

The empirical results of the Progressive Tiered Ablation Benchmark quantify the dramatic economic disparity between **unconstrained prompt-based code generation (Vanilla Baseline)** and **structured skill execution (Skillware Equipped)**.

Across the 23-model benchmark roster:
- **Vanilla Baseline consumed 3,087,129 tokens**.
- **Skillware Equipped consumed 1,500,967 tokens**.
- **Net reduction: 1,586,162 tokens eliminated (51.4% overall token reduction)**.
- **Workspace code debugging attempts: 464 scripts in Vanilla vs. 0 in Skillware (100% elimination)**.

## Token Context Expansion vs. Compaction

### The Vanilla Retry Blowout
In Vanilla mode, when a model's synthesized script fails with an exception (e.g. `KeyError`, `IndexError`, or `urllib.error.HTTPError`), the harness appends the script stdout, stderr, and exit code back into the conversation context. This triggers a compounding feedback loop:

1. **Turn 1**: 2,500 tokens (initial prompt + first script).
2. **Turn 2**: 5,200 tokens (script + full error stack trace + second script).
3. **Turn 3**: 8,900 tokens (accumulated trace history + third script).
4. **Turn 4+**: 15,000 to 50,000 tokens (context blowout, degraded attention, hallucinations).

This runaway token consumption was particularly pronounced in models like **Qwen 3.8 Flash** (burned 331,130 tokens in Vanilla vs 75,924 in Skillware, **77.1% reduction**) and **Meta Muse Spark 1.3** (burned 240,513 tokens in Vanilla vs 80,615 in Skillware, **66.5% reduction**).

### The Skillware Constant Footprint
Under Skillware, operations return structured, bounded JSON envelopes. If a parameter is invalid, schema validation halts the call immediately without executing arbitrary code or bloating context with stack traces. Most Skillware layers completed in 2 to 3 turns with bounded token overhead.

## Script Debugging Elimination Table

The table below shows the total number of workspace scripts written, executed, and debugged by each model in Vanilla Baseline compared to Skillware:

| Model | Vanilla Scripts Debugged | Skillware Scripts Debugged | Code Overhead Eliminated |
| :--- | :---: | :---: | :---: |
| **Qwen 3.8 Flash** | 48 | 0 | 100% |
| **Tencent Hunyuan 4 Preview** | 45 | 0 | 100% |
| **Google Gemini 3.8 Flash** | 43 | 0 | 100% |
| **DeepSeek v4.1 Flash (1017)** | 41 | 0 | 100% |
| **Meta Muse Spark 1.3** | 41 | 0 | 100% |
| **Xiaomi MiMo v2.6 Pro** | 36 | 0 | 100% |
| **NVIDIA Nemotron 3 Ultra 550B** | 27 | 0 | 100% |
| **Z-AI GLM 5.3 Flash** | 25 | 0 | 100% |
| **xAI Grok 4.7** | 24 | 0 | 100% |
| **Google Gemma 4 31B IT** | 24 | 0 | 100% |
| **NVIDIA Nemotron 3.5 Lightning** | 21 | 0 | 100% |
| **Anthropic Claude Haiku 5.5** | 16 | 0 | 100% |
| **Google Gemini 4 Argon** | 16 | 0 | 100% |
| **Qwen 3.6 35B A3B** | 16 | 0 | 100% |
| **DeepSeek v4 Pro** | 11 | 0 | 100% |
| **Z-AI GLM 5.3** | 10 | 0 | 100% |
| **Meta Llama 3.3 70B Instruct** | 10 | 0 | 100% |
| **Xiaomi MiMo v2.6 Flash** | 7 | 0 | 100% |
| **Anthropic Claude Sonnet 5** | 2 | 0 | 100% |
| **Meta Llama 4 Scout** | 1 | 0 | 100% |
| **OpenAI GPT-6 Luna** | 0 | 0 | N/A |
| **Meta Llama 3.1 8B Instruct** | 0 | 0 | N/A |
| **Meta Llama 4 Maverick** | 0 | 0 | N/A |
| **TOTAL** | **464** | **0** | **100%** |

## Latency and Cost Efficiency

- **Cumulative Latency**: Dropped from 6,914.7 seconds (115.2 minutes) to 4,331.4 seconds (72.2 minutes), representing a **1.60x overall execution speedup**.
- **Financial Savings**: Reduced upstream API cost by 41.8% on commercial endpoints, while dramatically improving throughput on sovereign self-hosted hardware.

## Visual Overview

```
[Figure: Cumulative Token Consumption and Context Growth Curves]
Reference: ../figures/token_consumption_curves.png
```
