# Skillware-Bench Documentation Hub

Welcome to the technical documentation and empirical findings repository for **Skillware-Bench**, the transparent benchmark harness evaluating sovereign and frontier AI models executing governed agent skills.

## Master Documentation Sitemap

### 1. Empirical Results & Cross-Model Standings
- [Master Leaderboard](leaderboard.md): Complete benchmark rankings and standings across the 23-model fleet.
- [Cross-Model Benchmark Overview](results/overview.md): Comprehensive 23-model cross-comparison tables, overall rankings, and capability tier breakdowns.
- [Complete Benchmark Exhibits Catalog](exhibits.md): Master catalog of all 46 active publication figures and tables (with high-res PNG previews) alongside 19 deferred exhibits.
- [Small Models + Skillware vs Frontier LLMs Alone](results/frontiers_vs_small.md): Empirical proof that compact sovereign models with deterministic skills match or outperform unassisted frontier APIs.
- [Execution Latency, Throughput & Cryptographic Audit Spine](results/latency_and_auditability.md): Deep-dive into execution latency, concurrency throughput scaling, tail latency compression, and AURA attestation overhead.
- [Behavioral Contracts, Safety Gating & Error Modes](results/behavioral_contracts.md): In-depth examination of the 4 simulation crucibles, base64 MIME attachment traps, confirmation gating, and injection resilience.
- [Token Economics & Overhead Work Avoided](results/token_economics.md): Detailed analysis of the 464 workspace scripts debugged in Vanilla vs 0 in Skillware, token compression curves, and cost savings.

### 2. Individual Model Cards (23 Models)
Detailed scorecards with 16-layer breakdowns, behavioral observations, and tamper-evident AURA cryptographic receipts:

- **Anthropic**: [Claude Sonnet 5](results/models/anthropic_claude_sonnet_5.md) • [Claude Haiku 5.5](results/models/anthropic_claude_haiku_5_5.md)
- **DeepSeek**: [DeepSeek v4.1 Flash (1017)](results/models/deepseek_v4_1_flash_1017.md) • [DeepSeek v4 Pro](results/models/deepseek_v4_pro.md)
- **Google**: [Gemini 4 Argon](results/models/google_gemini_4_argon.md) • [Gemini 3.8 Flash](results/models/google_gemini_3_8_flash.md) • [Gemma 4 31B IT](results/models/google_gemma_4_31b_it.md)
- **Meta**: [Llama 3.3 70B Instruct](results/models/meta_llama_3_3_70b_instruct.md) • [Llama 3.1 8B Instruct](results/models/meta_llama_3_1_8b_instruct.md) • [Llama 4 Scout](results/models/meta_llama_4_scout.md) • [Llama 4 Maverick](results/models/meta_llama_4_maverick.md) • [Muse Spark 1.3](results/models/meta_muse_spark_1_3.md)
- **NVIDIA**: [Nemotron 3 Ultra 550B](results/models/nvidia_nemotron_3_ultra_550b.md) • [Nemotron 3.5 Lightning](results/models/nvidia_nemotron_3_5_lightning.md)
- **OpenAI**: [GPT-6 Luna](results/models/openai_gpt_6_luna.md)
- **Qwen**: [Qwen 3.6 35B A3B](results/models/qwen_qwen3_6_35b_a3b.md) • [Qwen 3.8 Flash](results/models/qwen_qwen3_8_flash.md)
- **Tencent**: [Hunyuan 4 Preview](results/models/tencent_hy4_preview.md)
- **xAI**: [Grok 4.7](results/models/xai_grok_4_7.md)
- **Xiaomi**: [MiMo v2.6 Flash](results/models/xiaomi_mimo_v2_6_flash.md) • [MiMo v2.6 Pro](results/models/xiaomi_mimo_v2_6_pro.md)
- **Z-AI**: [GLM 5.3 Flash](results/models/zai_glm_5_3_flash.md) • [GLM 5.3](results/models/zai_glm_5_3.md)

### 3. Harness Architecture & Methodology
- [Benchmark Methodology & Harness Architecture](methodology.md): Mathematical formulation, agent economics, hermetic mock environment, and AURA cryptographic verification.
- [Simulation Crucibles Reference](crucibles.md): Technical definitions of the 4 benchmark crucibles and progressive tiers.

---

## Cryptographic Provenance

Every evaluation run is anchored with a deterministic SHA-256 causal DAG hash via the [AURA](https://github.com/arpahls/aura) attestation spine. Receipts ensure that all recorded turns, tool calls, token counts, and verdicts are tamper-evident and independently verifiable.
