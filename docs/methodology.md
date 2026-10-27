# Skillware-Bench Methodology & Technical Architecture

## Abstract

Skillware-Bench evaluates language models on realistic agent economics rather than abstract trivia or single-shot synthetic function schemas. It establishes an empirical baseline comparing **unconditioned, prompt-based code generation (Vanilla Baseline)** against **governed, deterministic skill execution (Skillware Equipped)** across progressive difficulty tiers.

### Figure 21 — The Skillware-Bench Measurement Harness Architecture

<div align="center">
  <img src="figures/fig21_measurement_harness.png" alt="Figure 21 — The Skillware-Bench Measurement Harness" width="100%" />
</div>

<br />

> **Figure 21.** The Skillware-Bench measurement harness. 23 frontier and sovereign model adapters evaluate across a 16-layer progressive ablation matrix (4 crucibles × 4 difficulty tiers, 736 conditions). Two parallel execution rails compare unconditioned code generation (vanilla track: Python synthesis, 30s timeout sandbox, AST unified diffs) against governed execution (equipped track: typed skill bundles, JSON/BNF schema validation, deterministic JIT handlers). Every trial executes within an isolated hermetic execution sandbox (air-gapped workspaces, ephemeral Port 0 mock APIs), scored by multi-vector state diff evaluators and cryptographically anchored by the AURA AuditSpine.

---

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

### Table 3 — The Four-Tier Progressive Difficulty Matrix

<div align="center">
  <img src="figures/tab03_progressive_difficulty_tiers.png" alt="Table 3 — The Four-Tier Progressive Difficulty Matrix" width="100%" />
</div>

<br />

> **Table 3.** The four-tier progressive difficulty matrix across 16 evaluated layers (averaged across 23 models under 736 conditions). Tiers test progression from atomic tool calls to multi-step DAG execution, confirmation gates, and adversarial injection. Unassisted models collapse in Tiers 2 and 3 when forced to write ad-hoc Python code to parse multi-step binary streams (464 scripts debugged). Skillware provides deterministic schema contracts, pre-compiled binary handlers, and immutable constitutional gates, delivering a +17.4% lift in Tier 2 and lifting aggregate benchmark pass rate from 81.5% to 91.6%.

### 2. Anatomy of a Skill Bundle

Rather than injecting monolithic system prompts, know-how in Skillware is compiled into self-contained, typed bundles:

### Figure 2 — Anatomical Breakdown of a First-Class Skill Bundle

<div align="center">
  <img src="figures/fig02_bundle_anatomy.png" alt="Figure 2 — Anatomy of a Skill Bundle" width="100%" />
</div>

<br />

> **Figure 2.** Anatomy of a Skillware skill bundle, exemplified by finance/uk_companies_house_handler . Know-how is decomposed into five first-class primitives rather than monolithic prompts: Contract ( manifest.yaml declares 12 typed actions, parameter JSON schemas, and permissions), Effect ( skill.py implements deterministic API execution, pagination, and bounded in-memory bytes), Directive ( instructions.md provides SOP guidance, disambiguation rules, and progressive disclosure), Assurance ( test_skill.py provides hermetic pytest fixtures and schema consistency invariants), and Corpus ( data/ stores domain reference lexicons such as UK/US terminology mappings). This atomic structure enables portable loading across diverse host agent runtimes with zero external dependencies.

### 3. Realistic Agent Economics

The benchmark models the true operating cost of enterprise and sovereign agent deployments:

- **Vanilla Baseline**: The model is provided raw environment primitives (`execute_python` in an isolated workspace, `http_request` for raw REST dispatch). It must discover endpoints, write complete Python scripts, parse JSON payloads, decode base64 attachments, and debug its own stack traces upon failure. Every failed script appends error logs to the conversation context, creating realistic token bloat.
- **Skillware Equipped**: The model is equipped with typed, validated skill manifests compiled from the Skillware registry. Operations execute in 1 to 2 turns with verified schema bounds and constitutional safety gating, eliminating raw script synthesis.

### 4. Hermetic Execution Sandbox
To ensure 100% reproducible, non-flaky evaluations without external network dependencies, Skillware-Bench executes all trials inside a multi-tenant hermetic execution sandbox:

- **Ephemeral Port 0 Mock Server**: An in-memory REST service (`HermeticMockServer`) dynamically binding to `127.0.0.1:0` that simulates Companies House, Mock IMAP/SMTP mail server, crypto AML sanction screening, and firewall endpoints offline.
- **Air-Gapped Workspaces**: Isolated scratchpad filesystems per condition (`workspaces/<model>/<scenario>/tier_<N>/`), ensuring zero leakage of state or credentials.
- **State Diff Tracking**: Maintains isolated per-tier state, tracking staged email drafts, physical sent messages, and disk-level mutations.

### 5. Cryptographic Attestation & Audit Spine via AURA
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

---

## Reproduction Guide

To run a complete 16-layer tiered ablation benchmark for any supported model:

```bash
# Run single model
python scripts/run_tiered_ablation_bench.py --model anthropic/claude-sonnet-5

# Run sovereign model locally or via OpenRouter
python scripts/run_tiered_ablation_bench.py --model qwen/qwen3.6-35b-a3b
```

---

## Technical Documentation Sitemap

- [Master Leaderboard](leaderboard.md)
- [Cross-Model Benchmark Overview](results/overview.md)
- [Complete Benchmark Exhibits Catalog](exhibits.md)
- [Simulation Crucibles Deep-Dive](crucibles.md)
- [Small Models + Skillware vs Frontier LLMs Alone](results/frontiers_vs_small.md)
- [Execution Latency, Throughput & Cryptographic Audit Spine](results/latency_and_auditability.md)
- [Behavioral Contracts, Safety Gating & Error Modes](results/behavioral_contracts.md)
- [Token Economics & Overhead Work Avoided](results/token_economics.md)
