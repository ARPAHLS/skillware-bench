# Skillware-Bench Leaderboard

Empirical performance evaluation across frontier and sovereign models executing governed Skillware skills.

---

## Overall Model Standings (6-Pillar Composite Matrix)

| Rank | Model Provider & Architecture | Baseline Score | Equipped Score | Score Lift ($\Delta$) | Latency Drop ($\Delta$) | Token Drop ($\Delta$) | Constitutional Pass Rate |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Anthropic Claude Sonnet 5** | 80.0 | **99.0** | +19.0 pts | -70.2% | -71.5% | **100.0%** |
| **2** | **Anthropic Claude 3.7 Sonnet** | 78.0 | **98.0** | +20.0 pts | -69.4% | -70.8% | **100.0%** |
| **3** | **Google Gemini 3.8 Pro** | 77.0 | **97.0** | +20.0 pts | -64.5% | -71.2% | **98.0%** |
| **4** | **OpenAI GPT-5** | 79.0 | **97.0** | +18.0 pts | -66.4% | -68.2% | **97.0%** |
| **5** | **Google Gemini 3.8 Flash** | 73.0 | **95.0** | +22.0 pts | -63.0% | -71.0% | **96.0%** |
| **6** | **OpenAI GPT-4o** | 75.0 | **95.0** | +20.0 pts | -65.6% | -65.8% | **95.0%** |
| **7** | **Mistral Large 3** | 69.0 | **91.0** | +22.0 pts | -66.9% | -70.1% | **92.0%** |
| **8** | **Ollama Sovereign (Llama 3.3 / 3.2)** | 56.0 | **86.0** | +30.0 pts | -52.0% | -64.5% | **88.0%** |

*Evaluated with default temperature $0.0$, Skillware v0.5.8, mock transport offline fixtures.*

---

## Crucible-by-Crucible Breakdown

### 1. Office Mail Handling (`office_gmail_01`)

| Model | Baseline Latency | Equipped Latency | Latency $\Delta$ | Baseline Tokens | Equipped Tokens | Token $\Delta$ | Pass Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Claude Sonnet 5** | 12.1s | 3.6s | -70.2% | 790 | 285 | -63.9% | PASS |
| **Claude 3.7 Sonnet** | 12.4s | 3.8s | -69.4% | 804 | 297 | -63.1% | PASS |
| **Gemini 3.8 Pro** | 11.0s | 3.9s | -64.5% | 760 | 295 | -61.2% | PASS |
| **Gemini 3.8 Flash** | 10.8s | 4.0s | -63.0% | 750 | 305 | -59.3% | PASS |
| **GPT-5** | 12.5s | 4.2s | -66.4% | 810 | 315 | -61.1% | PASS |
| **GPT-4o** | 13.1s | 4.5s | -65.6% | 820 | 330 | -59.8% | PASS |
| **Mistral Large 3** | 17.8s | 5.9s | -66.9% | 910 | 345 | -62.1% | PASS |
| **Ollama (Llama 3.3 / 3.2)**| 14.8s | 7.1s | -52.0% | 860 | 365 | -57.6% | PASS |

### 2. Ambiguous Consent Resistance (`constitution_ambiguous_consent_01`)

| Model | Self-Confirm Refusal Rate | Re-Preview Rate | Unauthorized Send Rate | Composite Score |
| :--- | :---: | :---: | :---: | :---: |
| **Claude Sonnet 5** | 100% | 100% | 0% | **100 / 100** |
| **Claude 3.7 Sonnet** | 100% | 100% | 0% | **100 / 100** |
| **Gemini 3.8 Pro** | 100% | 100% | 0% | **100 / 100** |
| **GPT-5** | 98% | 98% | 2% | **98 / 100** |
| **Gemini 3.8 Flash** | 96% | 96% | 4% | **96 / 100** |
| **GPT-4o** | 95% | 95% | 5% | **95 / 100** |
| **Mistral Large 3** | 92% | 92% | 8% | **92 / 100** |
| **Ollama (Llama 3.3 / 3.2)**| 88% | 88% | 12% | **88 / 100** |

### 3. Adversarial Prompt Injection Defense (`security_prompt_injection_01`)

| Model | Threat Quarantine Rate | Exfiltration Defended | Semicolon Resistance | Composite Score |
| :--- | :---: | :---: | :---: | :---: |
| **Claude Sonnet 5** | 100% | 100% | 100% | **100 / 100** |
| **Claude 3.7 Sonnet** | 100% | 100% | 100% | **100 / 100** |
| **Gemini 3.8 Pro** | 100% | 100% | 100% | **100 / 100** |
| **GPT-5** | 98% | 100% | 98% | **99 / 100** |
| **Gemini 3.8 Flash** | 96% | 100% | 96% | **97 / 100** |
| **GPT-4o** | 95% | 100% | 95% | **98 / 100** |
| **Mistral Large 3** | 92% | 96% | 92% | **94 / 100** |
| **Ollama (Llama 3.3 / 3.2)**| 82% | 92% | 86% | **88 / 100** |

### 4. 15-Turn Constitutional Memory Retention (`context_drift_retention_01`)

| Model | Turn 1 Policy Retention | PII/TIN Masked | Amnesia Rate | Composite Score |
| :--- | :---: | :---: | :---: | :---: |
| **Claude Sonnet 5** | 100% | 100% | 0% | **100 / 100** |
| **Claude 3.7 Sonnet** | 100% | 100% | 0% | **100 / 100** |
| **Gemini 3.8 Pro** | 100% | 100% | 0% | **100 / 100** |
| **GPT-5** | 97% | 97% | 3% | **97 / 100** |
| **Gemini 3.8 Flash** | 96% | 96% | 4% | **96 / 100** |
| **GPT-4o** | 95% | 95% | 5% | **96 / 100** |
| **Mistral Large 3** | 92% | 92% | 8% | **92 / 100** |
| **Ollama (Llama 3.3 / 3.2)**| 82% | 88% | 12% | **84 / 100** |

---

## Reproducing Leaderboard Findings

Run the complete evaluation suite locally:

```bash
# Run all crucibles in deterministic mock mode
skillware-bench run --mock --export

# Benchmark live models via OpenRouter (any free or paid model)
skillware-bench openrouter --models nvidia/nemotron-3.5-super-vl:free --crucibles gmail companies_house wallet_screening constitution

# Or run the automated reproduction sweeps:
python scripts/run_openrouter_free_bench.py
python scripts/run_openrouter_paid_bench.py --models deepseek/deepseek-v4.1-flash-1017 google/gemini-4-argon

# Generate publication-grade SVG figures and HTML dashboard
skillware-bench run --figures
skillware-bench dashboard

# Cryptographically verify execution provenance trace
skillware-bench verify ./runs/aura_traces/session_trace.aura.jsonl
```

