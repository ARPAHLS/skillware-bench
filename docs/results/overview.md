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
| 1 | [Qwen 3.8 Flash](models/qwen_qwen3_8_flash.md) | Compact Workhorse | 13/16 | **16/16** | +18.8% | 77.1% | 2.28x | 48 |
| 2 | [Google Gemini 3.8 Flash](models/google_gemini_3_8_flash.md) | Compact Workhorse | 16/16 | **16/16** | +0.0% | 71.3% | 1.82x | 43 |
| 3 | [Z-AI GLM 5.3](models/zai_glm_5_3.md) | Sovereign Enterprise 70B+ | 15/16 | **16/16** | +6.2% | 69.8% | 2.35x | 10 |
| 4 | [Tencent Hunyuan 4 Preview](models/tencent_hy4_preview.md) | Sovereign Enterprise 70B+ | 14/16 | **16/16** | +12.5% | 61.0% | 1.65x | 45 |
| 5 | [DeepSeek v4 Pro](models/deepseek_v4_pro.md) | Frontier API | 15/16 | **16/16** | +6.2% | 57.9% | 1.92x | 11 |
| 6 | [Google Gemma 4 31B IT](models/google_gemma_4_31b_it.md) | Compact Workhorse | 13/16 | **16/16** | +18.8% | 54.9% | 2.28x | 24 |
| 7 | [NVIDIA Nemotron 3 Ultra 550B](models/nvidia_nemotron_3_ultra_550b.md) | Sovereign Enterprise 70B+ | 13/16 | **16/16** | +18.8% | 53.1% | 2.05x | 27 |
| 8 | [Qwen 3.6 35B A3B](models/qwen_qwen3_6_35b_a3b.md) | Compact Workhorse | 15/16 | **16/16** | +6.2% | 52.4% | 1.79x | 16 |
| 9 | [DeepSeek v4.1 Flash (1017)](models/deepseek_v4_1_flash_1017.md) | Compact Workhorse | 16/16 | **16/16** | +0.0% | 52.0% | 1.72x | 41 |
| 10 | [xAI Grok 4.7](models/xai_grok_4_7.md) | Frontier API | 14/16 | **16/16** | +12.5% | 51.6% | 1.69x | 24 |
| 11 | [Xiaomi MiMo v2.6 Pro](models/xiaomi_mimo_v2_6_pro.md) | Sovereign Enterprise 70B+ | 15/16 | **16/16** | +6.2% | 29.2% | 0.66x | 36 |
| 12 | [Meta Muse Spark 1.3](models/meta_muse_spark_1_3.md) | Compact Workhorse | 16/16 | **15/16** | +-6.2% | 66.5% | 1.86x | 41 |
| 13 | [OpenAI GPT-6 Luna](models/openai_gpt_6_luna.md) | Frontier API | 14/16 | **15/16** | +6.2% | 34.3% | 1.58x | 0 |
| 14 | [Xiaomi MiMo v2.6 Flash](models/xiaomi_mimo_v2_6_flash.md) | Compact Workhorse | 16/16 | **15/16** | +-6.2% | 33.3% | 1.26x | 7 |
| 15 | [Z-AI GLM 5.3 Flash](models/zai_glm_5_3_flash.md) | Compact Workhorse | 15/16 | **15/16** | +0.0% | 22.2% | 1.53x | 25 |
| 16 | [Google Gemini 4 Argon](models/google_gemini_4_argon.md) | Frontier API | 16/16 | **15/16** | +-6.2% | 10.4% | 1.33x | 16 |
| 17 | [Meta Llama 4 Maverick](models/meta_llama_4_maverick.md) | Sovereign Open-Weight 8B | 6/16 | **15/16** | +56.2% | -31.4% | 1.36x | 0 |
| 18 | [NVIDIA Nemotron 3.5 Lightning](models/nvidia_nemotron_3_5_lightning.md) | Compact Workhorse | 10/16 | **14/16** | +25.0% | 57.3% | 2.53x | 21 |
| 19 | [Anthropic Claude Haiku 5.5](models/anthropic_claude_haiku_5_5.md) | Compact Workhorse | 15/16 | **14/16** | +-6.2% | 32.0% | 1.55x | 16 |
| 20 | [Anthropic Claude Sonnet 5](models/anthropic_claude_sonnet_5.md) | Frontier API | 14/16 | **14/16** | +0.0% | 29.6% | 1.48x | 2 |
| 21 | [Meta Llama 3.3 70B Instruct](models/meta_llama_3_3_70b_instruct.md) | Sovereign Enterprise 70B+ | 8/16 | **12/16** | +25.0% | 42.6% | 2.05x | 10 |
| 22 | [Meta Llama 4 Scout](models/meta_llama_4_scout.md) | Sovereign Open-Weight 8B | 7/16 | **12/16** | +31.2% | -69.1% | 1.20x | 1 |
| 23 | [Meta Llama 3.1 8B Instruct](models/meta_llama_3_1_8b_instruct.md) | Sovereign Open-Weight 8B | 4/16 | **5/16** | +6.2% | 56.7% | 2.44x | 0 |

## Breakdowns by Capability Tier

### 1. Frontier API Models
Models hosted via proprietary commercial API endpoints (Claude Sonnet 5, GPT-6 Luna, Gemini 4 Argon, Grok 4.7, DeepSeek v4 Pro).

| Model | Vanilla Pass | Skillware Pass | Token Savings | Speedup | Scripts Debugged | Model Card |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Anthropic Claude Sonnet 5** | 14/16 | 14/16 | 29.6% | 1.48x | 2 | [Card](models/anthropic_claude_sonnet_5.md) |
| **OpenAI GPT-6 Luna** | 14/16 | 15/16 | 34.3% | 1.58x | 0 | [Card](models/openai_gpt_6_luna.md) |
| **Google Gemini 4 Argon** | 16/16 | 15/16 | 10.4% | 1.33x | 16 | [Card](models/google_gemini_4_argon.md) |
| **xAI Grok 4.7** | 14/16 | 16/16 | 51.6% | 1.69x | 24 | [Card](models/xai_grok_4_7.md) |
| **DeepSeek v4 Pro** | 15/16 | 16/16 | 57.9% | 1.92x | 11 | [Card](models/deepseek_v4_pro.md) |

### 2. Sovereign Enterprise 70B+
High-capacity enterprise-scale sovereign open-weight models (Llama 3.3 70B, Nemotron 3 Ultra 550B, GLM 5.3, MiMo 2.6 Pro, Hunyuan 4 Preview).

| Model | Vanilla Pass | Skillware Pass | Token Savings | Speedup | Scripts Debugged | Model Card |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Tencent Hunyuan 4 Preview** | 14/16 | 16/16 | 61.0% | 1.65x | 45 | [Card](models/tencent_hy4_preview.md) |
| **NVIDIA Nemotron 3 Ultra 550B** | 13/16 | 16/16 | 53.1% | 2.05x | 27 | [Card](models/nvidia_nemotron_3_ultra_550b.md) |
| **Z-AI GLM 5.3** | 15/16 | 16/16 | 69.8% | 2.35x | 10 | [Card](models/zai_glm_5_3.md) |
| **Xiaomi MiMo v2.6 Pro** | 15/16 | 16/16 | 29.2% | 0.66x | 36 | [Card](models/xiaomi_mimo_v2_6_pro.md) |
| **Meta Llama 3.3 70B Instruct** | 8/16 | 12/16 | 42.6% | 2.05x | 10 | [Card](models/meta_llama_3_3_70b_instruct.md) |

### 3. Compact Workhorses (14B-35B)
Compact sovereign models engineered for production efficiency and high throughput.

| Model | Vanilla Pass | Skillware Pass | Token Savings | Speedup | Scripts Debugged | Model Card |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **DeepSeek v4.1 Flash (1017)** | 16/16 | 16/16 | 52.0% | 1.72x | 41 | [Card](models/deepseek_v4_1_flash_1017.md) |
| **Qwen 3.6 35B A3B** | 15/16 | 16/16 | 52.4% | 1.79x | 16 | [Card](models/qwen_qwen3_6_35b_a3b.md) |
| **Qwen 3.8 Flash** | 13/16 | 16/16 | 77.1% | 2.28x | 48 | [Card](models/qwen_qwen3_8_flash.md) |
| **Google Gemma 4 31B IT** | 13/16 | 16/16 | 54.9% | 2.28x | 24 | [Card](models/google_gemma_4_31b_it.md) |
| **Google Gemini 3.8 Flash** | 16/16 | 16/16 | 71.3% | 1.82x | 43 | [Card](models/google_gemini_3_8_flash.md) |
| **Z-AI GLM 5.3 Flash** | 15/16 | 15/16 | 22.2% | 1.53x | 25 | [Card](models/zai_glm_5_3_flash.md) |
| **Xiaomi MiMo v2.6 Flash** | 16/16 | 15/16 | 33.3% | 1.26x | 7 | [Card](models/xiaomi_mimo_v2_6_flash.md) |
| **NVIDIA Nemotron 3.5 Lightning** | 10/16 | 14/16 | 57.3% | 2.53x | 21 | [Card](models/nvidia_nemotron_3_5_lightning.md) |
| **Anthropic Claude Haiku 5.5** | 15/16 | 14/16 | 32.0% | 1.55x | 16 | [Card](models/anthropic_claude_haiku_5_5.md) |
| **Meta Muse Spark 1.3** | 16/16 | 15/16 | 66.5% | 1.86x | 41 | [Card](models/meta_muse_spark_1_3.md) |

### 4. Sovereign Open-Weight 8B & Llama 4
Compact edge and next-generation sovereign models (Llama 3.1 8B, Llama 4 Scout, Llama 4 Maverick).

| Model | Vanilla Pass | Skillware Pass | Token Savings | Speedup | Scripts Debugged | Model Card |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Meta Llama 4 Maverick** | 6/16 | 15/16 | -31.4% | 1.36x | 0 | [Card](models/meta_llama_4_maverick.md) |
| **Meta Llama 4 Scout** | 7/16 | 12/16 | -69.1% | 1.20x | 1 | [Card](models/meta_llama_4_scout.md) |
| **Meta Llama 3.1 8B Instruct** | 4/16 | 5/16 | 56.7% | 2.44x | 0 | [Card](models/meta_llama_3_1_8b_instruct.md) |

## Thematic Deep-Dive Navigation

- [Small Models + Skillware vs Frontier LLMs Alone](frontiers_vs_small.md)
- [Behavioral Contracts, Safety Gating & Error Modes](behavioral_contracts.md)
- [Token Economics & Overhead Work Avoided](token_economics.md)
- [Benchmark Methodology & Harness Architecture](../methodology.md)
