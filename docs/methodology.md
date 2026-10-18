# Skillware-Bench Methodology & Technical Architecture

## Abstract

Skillware-Bench evaluates language models on realistic agent economics rather than abstract trivia or single-shot synthetic function schemas. It establishes an empirical baseline comparing **unconditioned, prompt-based code generation (Vanilla Baseline)** against **governed, deterministic skill execution (Skillware Equipped)** across progressive difficulty tiers.

## Core Architectural Pillars

### 1. The 16-Layer Progressive Ablation Matrix
Models are tested across 4 real-world crucibles, each spanning 4 difficulty tiers:

$$\text{Total Conditions} = 4 \text{ Scenarios} \times 4 \text{ Tiers} \times 2 \text{ Configurations (Vanilla vs. Skillware)} = 32 \text{ Conditions per Model}$$

Across 23 evaluated models, this produces **368 benchmark layers and 736 live experimental test conditions**.

| Scenario | Skill ID | Core Capability Tested |
| :--- | :--- | :--- |
| **UK Companies House Registry** | `finance/uk_companies_house_handler` | Entity resolution, statutory officer filtering, parent/subsidiary disambiguation, adversarial injection defense. |
| **Office Mailbox & Attachments** | `office/gmail_handler` | Search, MIME multipart attachment extraction to disk, governed confirmation gates, phishing defense. |
| **Crypto AML Sanction Screening** | `finance/wallet_screening` | OFAC sanctions verification, clean history scoring, invalid hex checksum validation, zero address leakage. |
| **Prompt Injection Firewall** | `security/prompt_injection_firewall` | Plaintext override detection, zero-width unicode smuggling, ROT13 obfuscation bypass, clean content excision. |

### 2. Realistic Agent Economics

The benchmark models the true operating cost of enterprise and sovereign agent deployments:

- **Vanilla Baseline**: The model is provided raw environment primitives (`execute_python` in an isolated workspace, `http_request` for raw REST dispatch). It must discover endpoints, write complete Python scripts, parse JSON payloads, decode base64 attachments, and debug its own stack traces upon failure. Every failed script appends error logs to the conversation context, creating realistic token bloat.
- **Skillware Equipped**: The model is equipped with typed, validated skill manifests compiled from the Skillware registry. Operations execute in 1 to 2 turns with verified schema bounds and constitutional safety gating, eliminating raw script synthesis.

### 3. Hermetic Mock Environment
To ensure 100% reproducible, non-flaky evaluations without external network dependencies, Skillware-Bench runs an in-memory `HermeticMockServer`:

- Serves realistic REST mock endpoints on `http://127.0.0.1:51210`.
- Provides simulated Companies House REST endpoints, email search, attachment streaming, and Ethereum address lookups.
- Maintains isolated per-tier state, tracking staged email drafts, physical sent messages, and workspace disk changes.

### 4. Cryptographic Attestation & Audit Spine via AURA
Every benchmark execution records a comprehensive audit trail (`report.json` and `workspaces/<model>/<scenario>/tier_<N>/transcript.jsonl`). To guarantee tamper-evident verification, each run is cryptographically anchored using [AURA](https://github.com/arpahls/aura) (`arpahls/aura`):

```json
{
  "run_id": "tiered_ablation_20261018_115330",
  "model": "deepseek/deepseek-v4.1-flash-1017",
  "aura_cryptographic_receipt": {
    "sha256": "298a440d4280ef78a917ea948d96b01c7b5131dc9eb2146f4c35dd8eab878f17",
    "engine": "AURA AuditSpine / SHA-256",
    "verified": true
  }
}
```

The SHA-256 hash covers the exact input configuration, step sequences, tool arguments, workspace outputs, and scoring verdicts, providing an immutable proof receipt.

## Reproduction Guide

To run a complete 16-layer tiered ablation benchmark for any supported model:

```bash
# Run single model
python scripts/run_tiered_ablation_bench.py --model anthropic/claude-sonnet-5

# Run sovereign model locally or via OpenRouter
python scripts/run_tiered_ablation_bench.py --model qwen/qwen3.6-35b-a3b
```
