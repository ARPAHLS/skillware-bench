# Cross-Model Benchmark Overview & Standings

Comprehensive empirical evaluation of 23 sovereign and frontier language models across the 16-layer Progressive Tiered Ablation Benchmark (4 real-world crucibles x 4 difficulty tiers = 16 layers, 32 evaluated conditions per model; 368 total layers, 736 live experimental test conditions).

## Grand Aggregate Benchmark Metrics

| Metric | Vanilla Baseline | Skillware Equipped | Delta / Efficiency |
| :--- | :---: | :---: | :---: |
| **Total Evaluated Layers** | 368 | 368 | 736 conditions |
| **Overall Pass Rate** | 300/368 (81.5%) | **337/368 (91.6%)** | **+10.1% overall lift** |
| **Total Tokens Consumed** | 3,087,129 | **1,500,967** | **1,586,162 tokens saved (51.4% reduction)** |
| **Total Cumulative Latency** | 6914.7s (115.2m) | **4331.4s (72.2m)** | **1.60x execution speedup** |
| **Workspace Code Debugging Attempts** | 464 scripts debugged | **0 scripts** | **100% code debugging eliminated** |

## Master Cross-Model Standings

| Rank | Model Architecture | Capability Tier | Vanilla Pass | Skillware Pass | Pass Lift | Token Savings | Speedup | Vanilla Scripts |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | [Qwen 3.8 Flash](models/qwen_qwen3_8_flash.md) | Compact | 13/16 | **16/16** | +18.8% | 77.1% | 2.28x | 48 |
| 2 | [Google Gemini 3.8 Flash](models/google_gemini_3_8_flash.md) | Compact | 16/16 | **16/16** | +0.0% | 71.3% | 1.82x | 43 |
| 3 | [Z-AI GLM 5.3](models/zai_glm_5_3.md) | Enterprise | 15/16 | **16/16** | +6.2% | 69.8% | 2.35x | 10 |
| 4 | [Tencent Hunyuan 4 Preview](models/tencent_hy4_preview.md) | Enterprise | 14/16 | **16/16** | +12.5% | 61.0% | 1.65x | 45 |
| 5 | [DeepSeek v4 Pro](models/deepseek_v4_pro.md) | Frontier | 15/16 | **16/16** | +6.2% | 57.9% | 1.92x | 11 |
| 6 | [Google Gemma 4 31B IT](models/google_gemma_4_31b_it.md) | Edge | 13/16 | **16/16** | +18.8% | 54.9% | 2.28x | 24 |
| 7 | [NVIDIA Nemotron 3 Ultra 550B](models/nvidia_nemotron_3_ultra_550b.md) | Enterprise | 13/16 | **16/16** | +18.8% | 53.1% | 2.05x | 27 |
| 8 | [Qwen 3.6 35B A3B](models/qwen_qwen3_6_35b_a3b.md) | Compact | 15/16 | **16/16** | +6.2% | 52.4% | 1.79x | 16 |
| 9 | [DeepSeek v4.1 Flash (1017)](models/deepseek_v4_1_flash_1017.md) | Compact | 16/16 | **16/16** | +0.0% | 52.0% | 1.72x | 41 |
| 10 | [xAI Grok 4.7](models/xai_grok_4_7.md) | Frontier | 14/16 | **16/16** | +12.5% | 51.6% | 1.69x | 24 |
| 11 | [Xiaomi MiMo v2.6 Pro](models/xiaomi_mimo_v2_6_pro.md) | Enterprise | 15/16 | **16/16** | +6.2% | 29.2% | 0.66x | 36 |
| 12 | [Meta Muse Spark 1.3](models/meta_muse_spark_1_3.md) | Compact | 16/16 | **15/16** | -6.2% | 66.5% | 1.86x | 41 |
| 13 | [OpenAI GPT-6 Luna](models/openai_gpt_6_luna.md) | Frontier | 14/16 | **15/16** | +6.2% | 34.3% | 1.58x | 0 |
| 14 | [Xiaomi MiMo v2.6 Flash](models/xiaomi_mimo_v2_6_flash.md) | Compact | 16/16 | **15/16** | -6.2% | 33.3% | 1.26x | 7 |
| 15 | [Z-AI GLM 5.3 Flash](models/zai_glm_5_3_flash.md) | Compact | 15/16 | **15/16** | +0.0% | 22.2% | 1.53x | 25 |
| 16 | [Google Gemini 4 Argon](models/google_gemini_4_argon.md) | Frontier | 16/16 | **15/16** | -6.2% | 10.4% | 1.33x | 16 |
| 17 | [Meta Llama 4 Maverick](models/meta_llama_4_maverick.md) | Compact | 6/16 | **15/16** | +56.2% | -31.4% | 1.36x | 0 |
| 18 | [NVIDIA Nemotron 3.5 Lightning](models/nvidia_nemotron_3_5_lightning.md) | Compact | 10/16 | **14/16** | +25.0% | 57.3% | 2.53x | 21 |
| 19 | [Anthropic Claude Haiku 5.5](models/anthropic_claude_haiku_5_5.md) | Compact | 15/16 | **14/16** | -6.2% | 32.0% | 1.55x | 16 |
| 20 | [Anthropic Claude Sonnet 5](models/anthropic_claude_sonnet_5.md) | Frontier | 14/16 | **14/16** | +0.0% | 29.6% | 1.48x | 2 |
| 21 | [Meta Llama 3.3 70B Instruct](models/meta_llama_3_3_70b_instruct.md) | Enterprise | 8/16 | **12/16** | +25.0% | 42.6% | 2.05x | 10 |
| 22 | [Meta Llama 4 Scout](models/meta_llama_4_scout.md) | Edge | 7/16 | **12/16** | +31.2% | -69.1% | 1.20x | 1 |
| 23 | [Meta Llama 3.1 8B Instruct](models/meta_llama_3_1_8b_instruct.md) | Edge | 4/16 | **5/16** | +6.2% | 56.7% | 2.44x | 0 |

---

## Benchmark Master Summaries

<div align="center">
  <img src="../figures/tab07_four_axis_summary.png" alt="Tab. 7 — Four-Axis Master Summary Across 12 Models" width="100%" />
</div>

> **Table 7.** Four-axis master operational summary across 12 representative model architectures alongside the 23-model grand fleet aggregate (736 live experimental conditions). Across all four operational tiers—Frontier APIs, Enterprise deployments, Compact workhorses, and Edge models—Skillware delivers simultaneous multi-dimensional gains: compressing token expenditure by 29.6% to 77.1%, speeding up end-to-end task execution by 1.36x to 2.35x, elevating composite benchmark pass rates from 81.5% to 91.6%, and completely eliminating workspace script debugging traps (464 scripts eliminated to 0). Shaded row highlights the open-weight capability paradox, where compact models achieve frontier-grade execution when equipped with deterministic tools.

<div align="center">
  <img src="../figures/fig25_capability_compression_heatmap.png" alt="Fig. 25 — Capability Compression Heatmap" width="100%" />
</div>

> **Figure 25.** Capability compression heatmap across all 23 evaluated models and 4 enterprise crucibles (736 live experimental conditions). Cells display exact empirical pass rate lift (Δ percentage points) when equipping baseline models with Skillware execution manifests. Across the fleet, Skillware produces a +10.1% grand aggregate pass lift (from 81.5% to 91.6% fleet success, 337/368 vs 300/368 tasks passed). Uplift is heavily concentrated in complex multi-step stateful workflows: Office Mail achieves a fleet lift of +22.8% (68.5% → 91.3%), and Companies House records +12.0% (75.0% → 87.0%). Compact open-weight models achieve the largest single gains—most notably Meta Llama 4 Maverick (+56.2% lift, from 37.5% to 93.8% across 16 tasks)—effectively closing the capability gap with unassisted frontier models at a fraction of inference cost. Models are sorted by Grand Mean lift descending, then vanilla baseline.

---

## Breakdowns by Capability Tier

### 1. Frontier Models
Models hosted via commercial API endpoints with state-of-the-art generalist reasoning (Claude Sonnet 5, GPT-6 Luna, Gemini 4 Argon, Grok 4.7, DeepSeek v4 Pro).

| Model | Vanilla Pass | Skillware Pass | Token Savings | Speedup | Scripts Debugged | Model Card |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Anthropic Claude Sonnet 5** | 14/16 | 14/16 | 29.6% | 1.48x | 2 | [Card](models/anthropic_claude_sonnet_5.md) |
| **OpenAI GPT-6 Luna** | 14/16 | 15/16 | 34.3% | 1.58x | 0 | [Card](models/openai_gpt_6_luna.md) |
| **Google Gemini 4 Argon** | 16/16 | 15/16 | 10.4% | 1.33x | 16 | [Card](models/google_gemini_4_argon.md) |
| **xAI Grok 4.7** | 14/16 | 16/16 | 51.6% | 1.69x | 24 | [Card](models/xai_grok_4_7.md) |
| **DeepSeek v4 Pro** | 15/16 | 16/16 | 57.9% | 1.92x | 11 | [Card](models/deepseek_v4_pro.md) |

### 2. Enterprise Models
High-capacity sovereign enterprise models designed for on-premise and private cloud deployments (Nemotron 3 Ultra 550B, GLM 5.3, Hunyuan 4 Preview, MiMo v2.6 Pro, Llama 3.3 70B Instruct).

| Model | Vanilla Pass | Skillware Pass | Token Savings | Speedup | Scripts Debugged | Model Card |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Tencent Hunyuan 4 Preview** | 14/16 | 16/16 | 61.0% | 1.65x | 45 | [Card](models/tencent_hy4_preview.md) |
| **NVIDIA Nemotron 3 Ultra 550B** | 13/16 | 16/16 | 53.1% | 2.05x | 27 | [Card](models/nvidia_nemotron_3_ultra_550b.md) |
| **Z-AI GLM 5.3** | 15/16 | 16/16 | 69.8% | 2.35x | 10 | [Card](models/zai_glm_5_3.md) |
| **Xiaomi MiMo v2.6 Pro** | 15/16 | 16/16 | 29.2% | 0.66x | 36 | [Card](models/xiaomi_mimo_v2_6_pro.md) |
| **Meta Llama 3.3 70B Instruct** | 8/16 | 12/16 | 42.6% | 2.05x | 10 | [Card](models/meta_llama_3_3_70b_instruct.md) |

### 3. Compact Models
Compact sovereign models engineered for production cost efficiency, low latency, and high-throughput execution (Qwen 3.8 Flash, Gemini 3.8 Flash, Meta Llama 4 Maverick, DeepSeek v4.1 Flash, Qwen 3.6 35B A3B, GLM 5.3 Flash, MiMo v2.6 Flash, Muse Spark 1.3, Nemotron 3.5 Lightning, Claude Haiku 5.5).

| Model | Vanilla Pass | Skillware Pass | Token Savings | Speedup | Scripts Debugged | Model Card |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **DeepSeek v4.1 Flash (1017)** | 16/16 | 16/16 | 52.0% | 1.72x | 41 | [Card](models/deepseek_v4_1_flash_1017.md) |
| **Qwen 3.6 35B A3B** | 15/16 | 16/16 | 52.4% | 1.79x | 16 | [Card](models/qwen_qwen3_6_35b_a3b.md) |
| **Qwen 3.8 Flash** | 13/16 | 16/16 | 77.1% | 2.28x | 48 | [Card](models/qwen_qwen3_8_flash.md) |
| **Meta Llama 4 Maverick** | 6/16 | 15/16 | -31.4% | 1.36x | 0 | [Card](models/meta_llama_4_maverick.md) |
| **Google Gemini 3.8 Flash** | 16/16 | 16/16 | 71.3% | 1.82x | 43 | [Card](models/google_gemini_3_8_flash.md) |
| **Z-AI GLM 5.3 Flash** | 15/16 | 15/16 | 22.2% | 1.53x | 25 | [Card](models/zai_glm_5_3_flash.md) |
| **Xiaomi MiMo v2.6 Flash** | 16/16 | 15/16 | 33.3% | 1.26x | 7 | [Card](models/xiaomi_mimo_v2_6_flash.md) |
| **NVIDIA Nemotron 3.5 Lightning** | 10/16 | 14/16 | 57.3% | 2.53x | 21 | [Card](models/nvidia_nemotron_3_5_lightning.md) |
| **Anthropic Claude Haiku 5.5** | 15/16 | 14/16 | 32.0% | 1.55x | 16 | [Card](models/anthropic_claude_haiku_5_5.md) |
| **Meta Muse Spark 1.3** | 16/16 | 15/16 | 66.5% | 1.86x | 41 | [Card](models/meta_muse_spark_1_3.md) |

### 4. Edge Models
Compact edge and next-generation sovereign models operating on constrained compute footprints (Google Gemma 4 31B IT, Llama 4 Scout, Llama 3.1 8B Instruct).

| Model | Vanilla Pass | Skillware Pass | Token Savings | Speedup | Scripts Debugged | Model Card |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Google Gemma 4 31B IT** | 13/16 | 16/16 | 54.9% | 2.28x | 24 | [Card](models/google_gemma_4_31b_it.md) |
| **Meta Llama 4 Scout** | 7/16 | 12/16 | -69.1% | 1.20x | 1 | [Card](models/meta_llama_4_scout.md) |
| **Meta Llama 3.1 8B Instruct** | 4/16 | 5/16 | 56.7% | 2.44x | 0 | [Card](models/meta_llama_3_1_8b_instruct.md) |

---

## Crucible and Tier Lift Dynamics

<div align="center">
  <img src="../figures/fig13_gain_by_task_family.png" alt="Fig. 13 — Empirical Pass Rate Lift by Crucible" width="100%" />
</div>

> **Figure 13.** Empirical pass rate lift across domain crucibles and progressive difficulty tiers (23 models, 736 live experimental conditions). Terracotta bars highlight subgroups exceeding the grand benchmark mean (+10.1%), led by Office Mailbox (+22.8%) and Tier 2 DAG extraction (+17.4%), where unassisted models suffer catastrophic script debugging failure loops. Subgroups below the mean (sequential teal) show positive but narrower uplifts where baseline models already possessed adequate in-context reasoning.

---

## Thematic Deep-Dive Navigation

- [Complete Benchmark Exhibits Catalog](../exhibits.md)
- [Small Models + Skillware vs Frontier LLMs Alone](frontiers_vs_small.md)
- [Execution Latency, Throughput & Cryptographic Audit Spine](latency_and_auditability.md)
- [Behavioral Contracts, Safety Gating & Error Modes](behavioral_contracts.md)
- [Token Economics & Overhead Work Avoided](token_economics.md)
- [Benchmark Methodology & Harness Architecture](../methodology.md)
