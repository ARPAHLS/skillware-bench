# Skillware-Bench

The Transparent, Empirical Benchmark Harness for Governed Agent Skills.

Quantifying how frontier and sovereign language models execute real-world tasks, enforce constitutional safety gates, and eliminate token bloat.

## Benchmark Overview

Skillware-Bench evaluates models across an empirical **16-layer Progressive Tiered Ablation Benchmark** (4 real-world crucibles x 4 progressive difficulty tiers = 16 layers, 32 evaluated conditions per model). It contrasts **unconditioned code generation (Vanilla Baseline)** against **governed skill execution (Skillware Equipped)**.

Across the complete 23-model evaluation roster (spanning 11 sovereign and commercial model families), the benchmark comprises **368 total layers and 736 live experimental test conditions**.

## Grand Aggregate Results (23 Models, 736 Test Conditions)

| Metric | Vanilla Baseline | Skillware Equipped | Delta / Efficiency |
| :--- | :---: | :---: | :---: |
| **Total Evaluated Layers** | 368 | 368 | 736 live conditions |
| **Overall Pass Rate** | 300/368 (81.5%) | **337/368 (91.6%)** | **+10.1% overall lift** |
| **Total Tokens Consumed** | 3,087,129 | **1,500,967** | **1,586,162 tokens saved (51.4% reduction)** |
| **Total Cumulative Latency** | 6914.7s (115.2m) | **4331.4s (72.2m)** | **1.60x execution speedup** |
| **Workspace Scripts Debugged** | 464 scripts debugged | **0 scripts** | **100% code debugging eliminated** |

## Top 10 Model Standings

| Rank | Model Architecture | Capability Tier | Vanilla Pass | Skillware Pass | Pass Lift | Token Savings | Speedup | Vanilla Scripts |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | [Qwen 3.8 Flash](docs/results/models/qwen_qwen3_8_flash.md) | Compact Workhorse | 13/16 | **16/16** | +18.8% | 77.1% | 2.28x | 48 |
| 2 | [Google Gemini 3.8 Flash](docs/results/models/google_gemini_3_8_flash.md) | Compact Workhorse | 16/16 | **16/16** | +0.0% | 71.3% | 1.82x | 43 |
| 3 | [Z-AI GLM 5.3](docs/results/models/zai_glm_5_3.md) | Sovereign Enterprise 70B+ | 15/16 | **16/16** | +6.2% | 69.8% | 2.35x | 10 |
| 4 | [Tencent Hunyuan 4 Preview](docs/results/models/tencent_hy4_preview.md) | Sovereign Enterprise 70B+ | 14/16 | **16/16** | +12.5% | 61.0% | 1.65x | 45 |
| 5 | [DeepSeek v4 Pro](docs/results/models/deepseek_v4_pro.md) | Frontier API | 15/16 | **16/16** | +6.2% | 57.9% | 1.92x | 11 |
| 6 | [Google Gemma 4 31B IT](docs/results/models/google_gemma_4_31b_it.md) | Compact Workhorse | 13/16 | **16/16** | +18.8% | 54.9% | 2.28x | 24 |
| 7 | [NVIDIA Nemotron 3 Ultra 550B](docs/results/models/nvidia_nemotron_3_ultra_550b.md) | Sovereign Enterprise 70B+ | 13/16 | **16/16** | +18.8% | 53.1% | 2.05x | 27 |
| 8 | [Qwen 3.6 35B A3B](docs/results/models/qwen_qwen3_6_35b_a3b.md) | Compact Workhorse | 15/16 | **16/16** | +6.2% | 52.4% | 1.79x | 16 |
| 9 | [DeepSeek v4.1 Flash (1017)](docs/results/models/deepseek_v4_1_flash_1017.md) | Compact Workhorse | 16/16 | **16/16** | +0.0% | 52.0% | 1.72x | 41 |
| 10 | [xAI Grok 4.7](docs/results/models/xai_grok_4_7.md) | Frontier API | 14/16 | **16/16** | +12.5% | 51.6% | 1.69x | 24 |

*Full rankings across all 23 models are available in the [Cross-Model Benchmark Overview](docs/results/overview.md).*

## Key Empirical Findings

1. **Small Sovereign Models + Skillware Match or Outperform Frontier LLMs Alone**: Compact open-weight models (e.g. Qwen 3.6 35B, Gemma 4 31B, Nemotron 3.5 Lightning) equipped with deterministic skills consistently achieve higher pass rates (14-16/16) and lower latency than unassisted frontier APIs operating in Vanilla mode (e.g. Claude Sonnet 5, GPT-6 Luna, Grok 4.7). See [Frontiers vs Small Models Deep-Dive](docs/results/frontiers_vs_small.md).
2. **Elimination of the Base64 MIME Attachment Failure Trap**: Across nearly all frontier models in Vanilla mode, extracting binary email attachments caused catastrophic failures, triggering 5 to 11 debug attempts and burning tens of thousands of tokens. Skillware resolved attachments in 2 to 3 turns without executing any workspace scripts. See [Behavioral Contracts Analysis](docs/results/behavioral_contracts.md).
3. **100% Code Debugging Overhead Eliminated**: Vanilla models spent 464 iterations debugging raw Python scripts across the benchmark. Skillware completely eliminated this burden, reducing debugging iterations to zero. See [Token Economics Deep-Dive](docs/results/token_economics.md).

## Documentation Sitemap

- [Documentation Hub](docs/README.md)
- [Cross-Model Benchmark Overview (All 23 Models)](docs/results/overview.md)
- [Small Models + Skillware vs. Frontier LLMs Alone](docs/results/frontiers_vs_small.md)
- [Behavioral Contracts, Safety Gating & Error Modes](docs/results/behavioral_contracts.md)
- [Token Economics & Overhead Work Avoided](docs/results/token_economics.md)
- [Benchmark Methodology & Harness Architecture](docs/methodology.md)
- [23 Individual Model Cards](docs/results/models/)

## Quick Start & Reproduction

### Installation

```bash
git clone https://github.com/ARPAHLS/skillware-bench.git
cd skillware-bench
pip install -e .
```

### Running the Progressive Tiered Ablation Benchmark

```bash
# Run benchmark on any supported model
python scripts/run_tiered_ablation_bench.py --model deepseek/deepseek-v4.1-flash-1017

# Run on a compact sovereign model
python scripts/run_tiered_ablation_bench.py --model qwen/qwen3.6-35b-a3b
```

## Cryptographic Receipts via AURA

Every benchmark evaluation produces a verified cryptographic receipt anchored via the [AURA](https://github.com/arpahls/aura) attestation spine. Receipts contain a SHA-256 causal DAG hash over all executed turns, tool invocations, token metrics, and scoring outputs to ensure tamper-evident verification.

## License

MIT License. Copyright (c) 2026 ARPA Hellenic Logical Systems.
