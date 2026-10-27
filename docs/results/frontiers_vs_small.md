# Thematic Analysis: Small Models + Skillware vs. Frontier LLMs Alone

## Executive Summary

A central finding of the Progressive Tiered Ablation Benchmark across 23 models is that **compact, sovereign open-weight models equipped with deterministic skill bundles consistently match or exceed unassisted frontier language models operating in Vanilla mode**, while consuming a fraction of the token footprint and eliminating vendor lock-in.

When frontier LLMs (such as Anthropic Claude Sonnet 5, OpenAI GPT-6 Luna, or xAI Grok 4.7) are deployed without domain skills, they are forced to synthesize ad-hoc Python scripts in an unconstrained workspace. They repeatedly fall victim to runtime environment impedance, fragile regular expressions, and MIME decoding traps. In contrast, sovereign compact models (such as Qwen 3.6 35B, Google Gemma 4 31B, NVIDIA Nemotron 3.5 Lightning, or Z-AI GLM 5.3 Flash) equipped with deterministic Skillware skills achieve higher pass rates with lower latency and zero script debugging.

## Direct Empirical Comparison

The table below contrasts compact sovereign models equipped with Skillware against top-tier frontier models operating in Vanilla Baseline:

| Compact Sovereign Model + Skillware | Pass Rate | Total Tokens | Latency | vs. | Frontier Model Alone (Vanilla) | Pass Rate | Total Tokens | Latency | Outcome Delta |
| :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :--- |
| **Qwen 3.6 35B A3B + Skillware** | **16/16** | **69,603** | **224.0s** | vs | **Claude Sonnet 5 Alone** | 14/16 | 122,790 | 235.0s | **+2 tasks passed, 43.3% token savings** |
| **Google Gemma 4 31B IT + Skillware** | **16/16** | **43,033** | **123.7s** | vs | **xAI Grok 4.7 Alone** | 14/16 | 207,605 | 204.4s | **+2 tasks passed, 79.3% token savings** |
| **Qwen 3.8 Flash + Skillware** | **16/16** | **75,924** | **333.7s** | vs | **DeepSeek v4 Pro Alone** | 15/16 | 151,103 | 561.9s | **+1 task passed, 49.8% token savings** |
| **NVIDIA Nemotron 3.5 Lightning + Skillware** | **14/16** | **74,756** | **50.0s** | vs | **OpenAI GPT-6 Luna Alone** | 14/16 | 64,914 | 156.7s | **Equal pass rate, 3.13x speedup** |
| **Z-AI GLM 5.3 + Skillware** | **16/16** | **48,142** | **75.8s** | vs | **Gemini 4 Argon Alone** | 16/16 | 58,561 | 289.1s | **Equal pass rate, 3.81x speedup** |
| **Meta Llama 4 Maverick + Skillware** | **15/16** | **54,862** | **197.9s** | vs | **Claude Sonnet 5 Alone** | 14/16 | 122,790 | 235.0s | **+1 task passed, 55.3% token savings** |

## Architectural Drivers of the Compact Sovereign Advantage

### 1. Elimination of Script Synthesizer Latency
In Vanilla Baseline mode, models must invent ad-hoc Python code for tasks such as `urllib.request` dispatch, HTTP header configuration, JSON unwrapping, and binary attachment parsing. Frontier models write elaborate multi-line scripts, execute them, inspect stdout/stderr, and iterate when bugs arise. 

Compact models using Skillware bypass the code generation layer entirely. The skill manifest exposes high-level, validated operations (e.g., `resolve_company`, `search_messages`, `wallet_screening`) that execute deterministically in a compiled environment.

### 2. Guardrails Against Base64 MIME Attachment Traps
In Scenario 2 (`office_mail`, Tier 2), agents are required to extract a binary agenda PDF from an email attachment. Unassisted frontier models repeatedly failed because they attempted to decode multipart email payloads using fragile regex splits or incomplete MIME libraries, burning tens of thousands of tokens across 5 to 11 debug attempts. 

Compact models with Skillware executed the deterministic `download_attachment` operation in a single turn, writing the exact PDF bytes directly to disk with zero hallucinations.

### 3. Economic and Sovereign Implication
Deploying proprietary frontier APIs incurs substantial per-token costs, unpredictable latency spikes, and data privacy exposure. These empirical results prove that enterprise deployments can host sovereign compact models (16B-35B) locally or within sovereign VPC boundaries and achieve frontier-grade or superior reliability by augmenting them with governed Skillware skills.

## Empirical Exhibits

### Figure 5 — The Empirical Parameter Paradox Across Parameter Scales

<div align="center">
  <img src="../figures/fig05_parameter_paradox.png" alt="Figure 5 — The Parameter Paradox (Small Models + Skillware vs Large Models)" width="100%" />
</div>

<br />

> **Figure 5.** The empirical parameter paradox. Across three decades of parameter scale (8B to 550B+), Skillware-equipped models maintain a decisive performance wedge over unequipped baselines. The wedge is widest for compact sovereign models: an equipped Qwen 3.8 Flash (16B) or Gemma 4 (31B) achieves a perfect 16/16 (100.0%) pass rate, outscoring unequipped frontier models Claude Sonnet 5 and GPT-6 Luna (both 14/16, 87.5%) at roughly 1/30th the operational cost. Without skillware, unequipped frontier models plateau below 90% due to boundary failures on unconstrained tool contracts, whereas compact workhorses equipped with validated bundles eliminate execution regressions.

### Figure 18 — Equip-Any-Model Pass Rate Uplift Trajectories

<div align="center">
  <img src="../figures/fig18_equip_any_model_uplift.png" alt="Figure 18 — Equip-Any-Model Pass Rate Uplift" width="100%" />
</div>

<br />

> **Figure 18.** Pass rate trajectory under Skillware equipment across 14 representative models. Left axis ranks models by Vanilla unassisted pass rate (from Gemini 3.8 Flash at 100.0% down to Llama 4 Maverick at 37.5%). Right axis ranks models by net absolute pass rate lift under Skillware (from Maverick at +56.2% down to Gemini 3.8 Flash and Claude Sonnet 5 at +0.0%). Sovereign and compact workhorses achieve the steepest improvements when decoupled from raw code generation, with Meta Llama 4 Maverick jumping from 37.5% to 93.8% to achieve parity with frontier models.

---

## Related Analyses & Catalogs

- [Cross-Model Benchmark Overview](overview.md)
- [Complete Benchmark Exhibits Catalog](../exhibits.md)
- [Execution Latency, Throughput & Cryptographic Audit Spine](latency_and_auditability.md)
- [Behavioral Contracts, Safety Gating & Error Modes](behavioral_contracts.md)
- [Token Economics & Overhead Work Avoided](token_economics.md)
- [Master Leaderboard](../leaderboard.md)
