# Skillware-Bench Leaderboard

Empirical performance evaluation across 23 sovereign and frontier models executing governed Skillware skills under the 16-layer Progressive Tiered Ablation Benchmark.

---

> For complete cross-model tables, metric comparisons, and capability tier breakdowns, see the [Cross-Model Benchmark Overview](results/overview.md).

## Top Standings Summary

| Rank | Model Architecture | Capability Tier | Vanilla Pass | Skillware Pass | Pass Lift | Token Savings | Speedup | Model Card |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Google Gemini 3.8 Flash** | Compact | 16/16 | **16/16** | +0.0% | 71.3% | 1.82x | [Card](results/models/google_gemini_3_8_flash.md) |
| **2** | **DeepSeek v4.1 Flash (1017)** | Compact | 16/16 | **16/16** | +0.0% | 52.0% | 1.72x | [Card](results/models/deepseek_v4_1_flash_1017.md) |
| **3** | **Qwen 3.8 Flash** | Compact | 13/16 | **16/16** | +18.8% | 77.1% | 2.28x | [Card](results/models/qwen_qwen3_8_flash.md) |
| **4** | **Z-AI GLM 5.3** | Enterprise | 15/16 | **16/16** | +6.2% | 69.8% | 2.35x | [Card](results/models/zai_glm_5_3.md) |
| **5** | **Tencent Hunyuan 4 Preview** | Enterprise | 14/16 | **16/16** | +12.5% | 61.0% | 1.65x | [Card](results/models/tencent_hy4_preview.md) |
| **6** | **DeepSeek v4 Pro** | Frontier | 15/16 | **16/16** | +6.2% | 57.9% | 1.92x | [Card](results/models/deepseek_v4_pro.md) |
| **7** | **Google Gemma 4 31B IT** | Edge | 13/16 | **16/16** | +18.8% | 54.9% | 2.28x | [Card](results/models/google_gemma_4_31b_it.md) |
| **8** | **NVIDIA Nemotron 3 Ultra 550B** | Enterprise | 13/16 | **16/16** | +18.8% | 53.1% | 2.05x | [Card](results/models/nvidia_nemotron_3_ultra_550b.md) |
| **9** | **Qwen 3.6 35B A3B** | Compact | 15/16 | **16/16** | +6.2% | 52.4% | 1.79x | [Card](results/models/qwen_qwen3_6_35b_a3b.md) |
| **10** | **xAI Grok 4.7** | Frontier | 14/16 | **16/16** | +12.5% | 51.6% | 1.69x | [Card](results/models/xai_grok_4_7.md) |

*Full rankings across all 23 models are available in the [Cross-Model Benchmark Overview](results/overview.md).*

---

## Benchmark Standings & Trajectories

<div align="center">
  <img src="figures/tab04_eight_model_leaderboard.png" alt="Tab. 4 — Eight-Model Representative Benchmark Standings" width="100%" />
</div>

> **Table 4.** Eight-model representative benchmark standings, evaluated across 16 layers (32 live experimental conditions per model). Shaded row indicates the open-weight paradox entry (*token savings for Maverick measured per solved task: Vanilla solved 6/16 tasks; Skillware solved 15/16). Across both frontier APIs and compact workhorses, Skillware delivers positive pass rate lifts and substantial token compression: compact models like Qwen 3.8 Flash gain +18.8% to reach 100% pass rates at 1/30 operational cost (77.1% token savings), while Gemini 3.8 Flash retains 100% accuracy while eliminating 43 debugging scripts. Sovereign enterprise models (GLM 5.3, Hunyuan 4) reach 100% completion with up to 2.35x speedup, while Meta Llama 4 Maverick achieves the benchmark's largest single uplift (+56.2% lift, from 37.5% to 93.8%), overcoming cognitive paralysis on multi-step tool execution.

<div align="center">
  <img src="figures/fig18_equip_any_model_uplift.png" alt="Fig. 18 — Equip-Any-Model Pass Rate Uplift" width="100%" />
</div>

> **Figure 18.** Pass rate trajectory under Skillware equipment across 14 representative models. Left axis ranks models by Vanilla unassisted pass rate (from Gemini 3.8 Flash at 100.0% down to Llama 4 Maverick at 37.5%). Right axis ranks models by net absolute pass rate lift under Skillware (from Maverick at +56.2% down to Gemini 3.8 Flash and Claude Sonnet 5 at +0.0%). Sovereign and compact workhorses achieve the steepest improvements when decoupled from raw code generation, with Meta Llama 4 Maverick jumping from 37.5% to 93.8% to achieve parity with frontier models.

---

## Related Analyses & Catalogs

- [Cross-Model Benchmark Overview](results/overview.md)
- [Complete Benchmark Exhibits Catalog](exhibits.md)
- [Small Models + Skillware vs. Frontier LLMs Alone](results/frontiers_vs_small.md)
- [Execution Latency, Throughput & Cryptographic Audit Spine](results/latency_and_auditability.md)
- [Behavioral Contracts, Safety Gating & Error Modes](results/behavioral_contracts.md)
- [Token Economics & Overhead Work Avoided](results/token_economics.md)
- [Individual Model Cards](results/models/)
