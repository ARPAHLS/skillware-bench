# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-10-13

### Added

- **Anti-Contamination, Statistics & SVG Visualization Engine (Phase 4)**:
  - `PerturbationEngine`: Procedural anti-contamination generator varying entity names, corporate targets, and syntactic prompt templates while preserving invariant constitutional rules.
  - `StatisticalEvaluator` & Pass@k Estimator: Unbiased Pass@k calculation, 95% confidence intervals, and metric distributions across repeated runs.
  - `VisualGenerator`: Zero-dependency standalone SVG figure generator producing 10-Pillar Radar Plots (`radar_profile.svg`) and Empirical Delta Optimization charts (`empirical_lift_delta.svg`).
  - Automated Figure Export: Added `--figures` and `--figures-dir` CLI flags to `skillware-bench run` to export publication-grade SVG figures.

- **Adversarial Security & AURA Provenance Engine (Phase 3)**:

  - `PromptInjectionCrucible`: Bi-directional indirect prompt injection and semicolon ambush crucible stress-testing data exfiltration and isolation via `security/prompt_injection_firewall`.
  - `ContextDriftCrucible`: 15-turn long-horizon context drift crucible evaluating constitutional amnesia and PII/TIN retention under heavy conversational context.
  - `ProvenanceEngine`: Cryptographic Ed25519 trace signing and AURA `.aura.jsonl` causal hash chain verification engine detecting forged steps or log tampering.
  - Automated Regulatory Compliance Exporter: Generates formal compliance assessments mapped directly to EU AI Act Article 14 (Human Oversight) and ISO/IEC 42001 (AI Management Systems).
  - CLI `verify` & `export-compliance` Commands: Added `skillware-bench verify <trace>` and `skillware-bench export-compliance <trace> [--output <path>]`.
  - Automatic Trace Signing: `AgentLoop` automatically signs generated session logs upon completion, emitting immutable `.sig` receipts.

- **Live Zero-Mock Crucible Infrastructure & Execution Wiring (Phase 2)**:

  - `DisposableMailboxEnvironment`: Ephemeral test mail environment in `skillware_bench.infra` seeding realistic operational messages, MIME attachments (`agenda.pdf`), search filters, preview drafts, and gated dispatch.
  - `CompaniesHouseClient`: Live REST client against UK Companies House with embedded high-fidelity snapshot database for DeepMind Technologies (`07387824`), active director lookup, and filing history navigation.
  - `WalletScreeningClient`: Live on-chain query engine with canonical OFAC SDN sanctions list matching (Tornado Cash Router `0x85894...` critical flag vs Vitalik `0xd8dA6...` clean) and legal disclaimer verification.
  - `EvmTestnetFork`: Live JSON-RPC client and deterministic in-memory EVM testnet simulation supporting `eth_getBalance`, `eth_getCode`, contract bytecode verification, and on-chain risk profiles.
  - Bring-Your-Own-Model Dynamic Loader: Added `load_adapter_from_file()` and `--adapter <path.py>` flag in CLI to benchmark custom fine-tunes and proprietary models with zero boilerplate.
  - Live Multi-Turn Crucible Execution (`run_live`): Implemented native `run_live()` across all 5 simulation crucibles (`GmailWorkflowCrucible`, `CompaniesHouseCrucible`, `WalletScreeningCrucible`, `ConstitutionStressCrucible`, `ChainedPipelineCrucible`).
  - Dual-Engine Harness Integration: Connected `HarnessRunner.run_suite()` to execute `run_live()` against live models and real infrastructure when `--live` is active.


- **Live Model Execution Engine & Provider Adapters (Phase 1)**:
  - `BaseModelAdapter`: Abstract model execution interface with standardized `chat()` protocol and schema formatters.
  - `OpenAIAdapter`: Native function calling adapter for `gpt-4o`, `gpt-4o-mini`, `o3-mini`, and `o1`.
  - `AnthropicAdapter`: Structured tool use adapter for `claude-3-7-sonnet` and `claude-3-5-haiku`.
  - `GeminiAdapter`: Modern `google-genai` SDK integration with function declaration translation and cached token tracking for `gemini-2.5-pro` and `gemini-2.5-flash`.
  - `MistralAdapter`: Official `mistralai` SDK integration for `mistral-large-latest` and `codestral-latest`.
  - `OllamaAdapter`: Local sovereign model runner supporting `llama3.2` and `qwen2.5` with zero API cost.
  - `MockModelAdapter`: Fully scriptable mock adapter with simulated 429 rate limit errors for fault recovery testing.
  - Bring-Your-Own-Model (BYOM): `AdapterRegistry` and `get_adapter` factory enabling custom adapter plugins.
  - Precision Token Telemetry & Pricing Engine: Tracks prompt tokens, completion tokens, cached tokens, TTFT, and calculates exact USD costs based on live model pricing tables.
  - Resilient Retry Engine: `execute_with_retry` with exponential backoff and jitter to survive transient rate limits and server outages.

- **Universal Multi-Turn Agent Loop (`skillware_bench.core.agent_loop.AgentLoop`)**:
  - Full Skillware integration: loads skill bundles via `SkillLoader.load_skill()`, validates inputs against manifest schemas, and executes native skill logic.
  - Immutable Causal Provenance via AURA: wraps benchmark execution runs in `aura.api.Session`, generating cryptographically linked `.aura.jsonl` causal audit logs.
  - Teleological Goal Alignment via MnemoLink: embeds `Teleology` goal contracts into agent sessions.
  - Constitutional Safety Gates: intercepts irreversible actions requiring explicit confirmation before execution and checks against ambiguous consent.

- **CLI Enhancements & Environment Verification**:
  - Added `skillware-bench check-env` command with masked tabular verification for all provider API keys and RPC endpoints.
  - Added `--live` flag to `skillware-bench run` to switch between deterministic offline crucibles and real frontier model execution.
  - Automatic `.env` loading on CLI startup via `python-dotenv`.

- **Core Benchmark Architecture & Harness Engine**:
  - Multi-tier progression framework: Tier 1 (Deterministic Mocked Skills), Tier 2 (Tool-Selection & Schema Validity), Tier 3 (Constitutional Safety & Procedural Compliance), Tier 4 (Multi-Skill Pipeline Chaining), and Tier 5 (Model Economics: Cost, Latency, & Token Bloat).
  - A/B Comparative Crucible Engine: With-Skillware vs Without-Skillware (Generic Prompt) delta evaluation.

- **Real-World Simulation Crucibles**:
  - `Crucible 1: Gmail Workflow (office/gmail_handler)`: End-to-end recipient resolution, inbox search, preview-before-send gating, ambiguous consent resistance, and inbound prompt-injection defense.
  - `Crucible 2: UK Companies House (finance/uk_companies_house_handler)`: Deterministic entity search, officer/PSC extraction, filing history navigation, and anti-hallucination company number checks.
  - `Crucible 3: Crypto Wallet Screening (finance/wallet_screening)`: Sanctions checks (OFAC), mixer address screening, risk scoring, and non-legal advice disclaimer compliance.
  - `Crucible 4: Constitutional Safety & Boundary Gates`: Negative controls, unauthorized send blocking, `dry_run` enforcement, and prompt injection firewall resilience.
  - `Crucible 5: Chained Compliance Pipeline`: Multi-step extraction (`pii_masker` -> `uk_companies_house_handler` -> `token_limiter`).

- **Metrics & Reporting Engine**:
  - 6-pillar evaluation metric: Schema Accuracy, Procedural Sequence, Constitutional Compliance, Token Compression, Latency Acceleration, and Actionability.
  - Automated delta calculation and JSON report export.

- **Packaging & Cross-Version Compatibility**:
  - Added `skillware>=0.5.5`, `aura-harness>=0.3.5`, and `mnemolink>=0.2.3` to dependencies.
  - Added Python 3.10 TOML compatibility fallback for package integrity test.
  - Automated import path sanitizer preventing local repository shadowing of installed packages.

- **Repository Baseline & Brand Alignment**:
  - Standardized ARPA Hellenic Logical Systems branding, pastel badge styling, `CITATION.cff`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and MIT License.
  - Zero emojis throughout codebase, CLI output, and documentation.
