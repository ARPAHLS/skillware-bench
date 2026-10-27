# Skillware-Bench

<div align="center">
  <p>The Transparent, Empirical Benchmark Harness for Governed Agent Skills.</p>
  <p>Quantifying how frontier and sovereign language models execute real-world tasks, enforce constitutional safety gates, and eliminate token bloat.</p>
</div>

<br/>

<div align="center">
  <img src="https://img.shields.io/badge/License-MIT-efcefa?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Python-3.10+-bae6fd?style=flat-square" alt="Python Version">
  <a href="https://github.com/ARPAHLS/skillware-bench/actions/workflows/ci.yml"><img src="https://img.shields.io/badge/CI-passing-bbf7d0?style=flat-square" alt="CI Status"></a>
  <a href="https://github.com/arpahls/aura"><img src="https://img.shields.io/badge/Attestation-AURA-ffdac1?style=flat-square" alt="Attestation AURA"></a>
</div>

<br/>

<div align="center">
  <a href="#benchmark-overview">Overview</a> •
  <a href="#grand-aggregate-results-23-models-736-test-conditions">Grand Aggregate</a> •
  <a href="#top-10-model-standings">Leaderboard</a> •
  <a href="#key-empirical-findings">Key Findings</a> •
  <a href="#documentation-sitemap">Documentation</a> •
  <a href="#quick-start--reproduction">Quick Start</a> •
  <a href="#citing">Citing</a> •
  <a href="#license">License</a>
</div>

---

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

### Figure 25 — Capability Compression Heatmap Across the 23-Model Fleet

<div align="center">
  <img src="docs/figures/fig25_capability_compression_heatmap.png" alt="Figure 25 — Capability Compression Heatmap" width="100%" />
</div>

<br />

> **Figure 25.** Capability compression heatmap across all 23 evaluated models and 4 enterprise crucibles (736 live experimental conditions). Cells display exact empirical pass rate lift (&Delta; percentage points) when equipping baseline models with Skillware execution manifests. Across the fleet, Skillware produces a **+10.1% grand aggregate pass lift** (from 81.5% to 91.6% fleet success, 337/368 vs 300/368 tasks passed). Uplift is heavily concentrated in complex multi-step stateful workflows: **Office Mail** achieves a fleet lift of **+22.8%** (68.5% &rarr; 91.3%), and **Companies House** records **+12.0%** (75.0% &rarr; 87.0%). Compact open-weight models achieve the largest single gains—most notably Meta Llama 4 Maverick (+56.2% lift, from 37.5% to 93.8% across 16 tasks)—effectively closing the capability gap with unassisted frontier models at a fraction of inference cost. Models are sorted by Grand Mean lift descending, then vanilla baseline.

## Top 10 Model Standings

| Rank | Model Architecture | Capability Tier | Vanilla Pass | Skillware Pass | Pass Lift | Token Savings | Speedup | Vanilla Scripts |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | [Qwen 3.8 Flash](docs/results/models/qwen_qwen3_8_flash.md) | Compact | 13/16 | **16/16** | +18.8% | 77.1% | 2.28x | 48 |
| 2 | [Google Gemini 3.8 Flash](docs/results/models/google_gemini_3_8_flash.md) | Compact | 16/16 | **16/16** | +0.0% | 71.3% | 1.82x | 43 |
| 3 | [Z-AI GLM 5.3](docs/results/models/zai_glm_5_3.md) | Enterprise | 15/16 | **16/16** | +6.2% | 69.8% | 2.35x | 10 |
| 4 | [Tencent Hunyuan 4 Preview](docs/results/models/tencent_hy4_preview.md) | Enterprise | 14/16 | **16/16** | +12.5% | 61.0% | 1.65x | 45 |
| 5 | [DeepSeek v4 Pro](docs/results/models/deepseek_v4_pro.md) | Frontier | 15/16 | **16/16** | +6.2% | 57.9% | 1.92x | 11 |
| 6 | [Google Gemma 4 31B IT](docs/results/models/google_gemma_4_31b_it.md) | Edge | 13/16 | **16/16** | +18.8% | 54.9% | 2.28x | 24 |
| 7 | [NVIDIA Nemotron 3 Ultra 550B](docs/results/models/nvidia_nemotron_3_ultra_550b.md) | Enterprise | 13/16 | **16/16** | +18.8% | 53.1% | 2.05x | 27 |
| 8 | [Qwen 3.6 35B A3B](docs/results/models/qwen_qwen3_6_35b_a3b.md) | Compact | 15/16 | **16/16** | +6.2% | 52.4% | 1.79x | 16 |
| 9 | [DeepSeek v4.1 Flash (1017)](docs/results/models/deepseek_v4_1_flash_1017.md) | Compact | 16/16 | **16/16** | +0.0% | 52.0% | 1.72x | 41 |
| 10 | [xAI Grok 4.7](docs/results/models/xai_grok_4_7.md) | Frontier | 14/16 | **16/16** | +12.5% | 51.6% | 1.69x | 24 |

*Full rankings across all 23 models are available in the [Cross-Model Benchmark Overview](docs/results/overview.md).*

### Table 7 — Four-Axis Master Operational Summary

<div align="center">
  <img src="docs/figures/tab07_four_axis_summary.png" alt="Table 7 — Four-Axis Master Summary" width="100%" />
</div>

<br />

> **Table 7.** Four-axis master benchmark summary across 12 representative frontier and sovereign architectures (384 live conditions). Models are sorted by Skillware Accuracy descending within capability tiers. Pass lift reflects delta percentage points over unassisted Vanilla baselines. Token reduction captures total prompt and completion token savings. Speedup denotes wall-clock runtime acceleration. Code Debugging Eliminated denotes total elimination of ad-hoc bash and python script repair loops (464 loops fleet-wide in Vanilla vs 0 in Skillware).

## Key Empirical Findings

1. **Small Sovereign Models + Skillware Match or Outperform Frontier LLMs Alone**: Compact open-weight models (e.g. Qwen 3.6 35B, Gemma 4 31B, Nemotron 3.5 Lightning) equipped with deterministic skills consistently achieve higher pass rates (14-16/16) and lower latency than unassisted frontier APIs operating in Vanilla mode (e.g. Claude Sonnet 5, GPT-6 Luna, Grok 4.7). See [Frontiers vs Small Models Deep-Dive](docs/results/frontiers_vs_small.md).

<div align="center">
  <img src="docs/figures/fig12_cost_capability_frontier.png" alt="Figure 12 — Cost-Capability Frontier" width="100%" />
</div>

<br />

> **Figure 12.** The cost–capability frontier across eight representative models from the benchmark fleet. Each dashed trajectory connects a model from its Vanilla baseline (ochre) to its Skillware equipped operating point (emerald green). The Skillware frontier dominates the Vanilla fleet everywhere, shifting up (higher accuracy across 16 benchmark layers) and to the left (lower operational token cost per task).

2. **Elimination of the Base64 MIME Attachment Failure Trap**: Across nearly all frontier models in Vanilla mode, extracting binary email attachments caused catastrophic failures, triggering 5 to 11 debug attempts and burning tens of thousands of tokens. Skillware resolved attachments in 2 to 3 turns without executing any workspace scripts. See [Behavioral Contracts Analysis](docs/results/behavioral_contracts.md).

<div align="center">
  <img src="docs/figures/fig11_latency_anatomy.png" alt="Figure 11 — Latency Anatomy" width="100%" />
</div>

<br />

> **Figure 11.** Latency anatomy of a complex reference workflow (Office Mail Tier 2). JIT context excision shrinks prefill latency from 4.1 s to 0.7 s, compact model routing shortens decode from 6.2 s to 3.4 s, and deterministic host validation eliminates speculative error loops: end-to-end median latency falls from 14.2 s to 6.3 s (−55.6%). Time to first token (TTFT) collapses from 1.9 s to 0.4 s.

3. **100% Code Debugging Overhead Eliminated**: Vanilla models spent 464 iterations debugging raw Python scripts across the benchmark. Skillware completely eliminated this burden, reducing debugging iterations to zero. See [Token Economics Deep-Dive](docs/results/token_economics.md).

## Documentation Sitemap

- [Documentation Hub](docs/README.md)
- [Master Leaderboard](docs/leaderboard.md)
- [Cross-Model Benchmark Overview (All 23 Models)](docs/results/overview.md)
- [Complete Benchmark Exhibits Catalog](docs/exhibits.md)
- [Small Models + Skillware vs. Frontier LLMs Alone](docs/results/frontiers_vs_small.md)
- [Execution Latency, Throughput & Cryptographic Audit Spine](docs/results/latency_and_auditability.md)
- [Behavioral Contracts, Safety Gating & Error Modes](docs/results/behavioral_contracts.md)
- [Token Economics & Overhead Work Avoided](docs/results/token_economics.md)
- [Benchmark Methodology & Harness Architecture](docs/methodology.md)
- [Simulation Crucibles Reference](docs/crucibles.md)
- [23 Individual Model Cards](docs/results/models/)

## Quick Start & Reproduction

### Installation

```bash
git clone https://github.com/ARPAHLS/skillware-bench.git
cd skillware-bench
pip install -e .
```

### 1. Interactive CLI & Mock Execution (Zero API Keys Required)

```bash
# Launch interactive pastel menu
skillware-bench menu

# Execute offline deterministic simulation crucibles
skillware-bench run --mock

# Compare with-Skillware vs vanilla baseline turn-by-turn
skillware-bench compare --suite gmail

# Generate interactive inspection dashboard
skillware-bench dashboard --output ./runs/dashboard.html
```

### 2. Live Progressive Tiered Ablation Sweeps

```bash
# Run benchmark on any supported model via API
python scripts/run_tiered_ablation_bench.py --model deepseek/deepseek-v4.1-flash-1017

# Run on a compact sovereign model
python scripts/run_tiered_ablation_bench.py --model qwen/qwen3.6-35b-a3b
```

## Cryptographic Receipts via AURA

Every benchmark evaluation produces a verified cryptographic receipt anchored via the [AURA](https://github.com/arpahls/aura) attestation spine. Receipts contain a SHA-256 causal DAG hash over all executed turns, tool invocations, token metrics, and scoring outputs to ensure tamper-evident verification.

The complete canonical execution reports for all 23 evaluated models are tracked in [`benchmarks/reports/`](benchmarks/reports/README.md). Verify any model's receipt instantly without API keys:

```bash
skillware-bench verify benchmarks/reports/google_gemma_4_31b_it.json
```

## Citing

If you use Skillware-Bench in research or products, please cite it using [CITATION.cff](CITATION.cff) (GitHub **Cite this repository**). For reproducibility, also record the **Skillware-Bench version** you used (Git tag, for example `0.3.1`).

## License

MIT License. Copyright (c) 2026 ARPA Hellenic Logical Systems.
