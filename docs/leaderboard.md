# Skillware-Bench Leaderboard

Empirical performance evaluation across 23 sovereign and frontier models executing governed Skillware skills under the 16-layer Progressive Tiered Ablation Benchmark.

---

> For complete cross-model tables, metric comparisons, and capability tier breakdowns, see the [Cross-Model Benchmark Overview](results/overview.md).

## Top Standings Summary

| Rank | Model Architecture | Capability Tier | Vanilla Pass | Skillware Pass | Pass Lift | Token Savings | Speedup | Model Card |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Google Gemini 3.8 Flash** | Compact Workhorse | 16/16 | **16/16** | +0.0% | 71.3% | 1.82x | [Card](results/models/google_gemini_3_8_flash.md) |
| **2** | **DeepSeek v4.1 Flash (1017)** | Compact Workhorse | 16/16 | **16/16** | +0.0% | 52.0% | 1.72x | [Card](results/models/deepseek_v4_1_flash_1017.md) |
| **3** | **Qwen 3.8 Flash** | Compact Workhorse | 13/16 | **16/16** | +18.8% | 77.1% | 2.28x | [Card](results/models/qwen_qwen3_8_flash.md) |
| **4** | **Z-AI GLM 5.3** | Sovereign Enterprise 70B+ | 15/16 | **16/16** | +6.2% | 69.8% | 2.35x | [Card](results/models/zai_glm_5_3.md) |
| **5** | **Tencent Hunyuan 4 Preview** | Sovereign Enterprise 70B+ | 14/16 | **16/16** | +12.5% | 61.0% | 1.65x | [Card](results/models/tencent_hy4_preview.md) |
| **6** | **DeepSeek v4 Pro** | Frontier API | 15/16 | **16/16** | +6.2% | 57.9% | 1.92x | [Card](results/models/deepseek_v4_pro.md) |
| **7** | **Google Gemma 4 31B IT** | Compact Workhorse | 13/16 | **16/16** | +18.8% | 54.9% | 2.28x | [Card](results/models/google_gemma_4_31b_it.md) |
| **8** | **NVIDIA Nemotron 3 Ultra 550B** | Sovereign Enterprise 70B+ | 13/16 | **16/16** | +18.8% | 53.1% | 2.05x | [Card](results/models/nvidia_nemotron_3_ultra_550b.md) |
| **9** | **Qwen 3.6 35B A3B** | Compact Workhorse | 15/16 | **16/16** | +6.2% | 52.4% | 1.79x | [Card](results/models/qwen_qwen3_6_35b_a3b.md) |
| **10** | **xAI Grok 4.7** | Frontier API | 14/16 | **16/16** | +12.5% | 51.6% | 1.69x | [Card](results/models/xai_grok_4_7.md) |

## Related Analyses

- [Cross-Model Benchmark Overview](results/overview.md)
- [Small Models + Skillware vs. Frontier LLMs Alone](results/frontiers_vs_small.md)
- [Behavioral Contracts, Safety Gating & Error Modes](results/behavioral_contracts.md)
- [Token Economics & Overhead Work Avoided](results/token_economics.md)
- [Individual Model Cards](results/models/)
