# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-10-18

### Added

- **23-Model Grand Benchmark Suite (368 Layers, 736 Live Conditions)**:
  - Comprehensive empirical evaluation across 23 sovereign and frontier language models spanning 11 model families:
    - **Frontier APIs**: Anthropic Claude Sonnet 5, OpenAI GPT-6 Luna, Google Gemini 4 Argon, xAI Grok 4.7, DeepSeek v4 Pro.
    - **Compact Workhorses**: Qwen 3.8 Flash, Google Gemini 3.8 Flash, Google Gemma 4 31B IT, DeepSeek v4.1 Flash (1017), Z-AI GLM 5.3 Flash, Xiaomi MiMo v2.6 Flash, Anthropic Claude Haiku 5.5, Meta Muse Spark 1.3, NVIDIA Nemotron 3.5 Lightning.
    - **Sovereign Enterprise 70B+ & Open-Weight**: NVIDIA Nemotron 3 Ultra 550B, Z-AI GLM 5.3, Tencent Hunyuan 4 Preview, Xiaomi MiMo v2.6 Pro, Meta Llama 3.3 70B Instruct, Meta Llama 4 Scout, Meta Llama 4 Maverick, Meta Llama 3.1 8B Instruct, Qwen 3.6 35B A3B.
  - **Empirical Grand Results**:
    - Pass Rate: Vanilla 81.5% (300/368) vs. Skillware **91.6% (337/368)** (+10.1% overall pass lift).
    - Token Efficiency: Vanilla 3,087,129 tokens vs. Skillware **1,500,967 tokens** (1,586,162 tokens saved, **51.4% reduction**).
    - Latency: Vanilla 6,914.7s vs. Skillware **4,331.4s** (**1.60x overall speedup**).
    - Work Avoided: **464 workspace scripts debugged in Vanilla vs. 0 in Skillware** (100% code debugging overhead eliminated).
- **Progressive Tiered Ablation Benchmark Harness (`scripts/run_tiered_ablation_bench.py`)**:
  - Four progressive difficulty tiers: Tier 1 (Single Lookup), Tier 2 (Multi-Step Dependent Chain), Tier 3 (Disambiguation & Hierarchy), and Tier 4 (Adversarial Injection & Threat Neutralization).
  - Realistic Agent Economics: Replaced naive spoon-fed tools with raw agent primitives (`execute_python` and `http_request`). Vanilla models must discover endpoints, write complete scripts, debug runtime errors across turns, and absorb true context expansion costs.
  - Hermetic Mock Infrastructure (`HermeticMockServer`): Zero-cost, zero-collision local REST server dynamically binding to ephemeral OS Port 0, serving UK Companies House and Mailbox APIs without external dependencies.
  - Synthetic Ground-Truth Registries: `mock_companies_registry.py` (10 corporate archetypes including active operating subsidiaries, holding vehicles, and dissolved entities) and `mock_inbox_registry.py` (20 operational messages, binary attachments, and prompt injection vectors).
  - Multi-Turn Workspace Isolation & Forensic Audit Trail: Air-gapped workspaces per tier archiving all script attempts (`attempt_1.py` through `attempt_8.py`), unified diff patches (`diff_k_to_k+1.patch`), stdout, stderr, exit codes, and AURA SHA-256 cryptographic trace receipts.
  - Full 4-Scenario x 4-Tier (16-Layer) Benchmark Architecture: Expanded benchmark coverage to 4 core real-world domains (16 tiers, 32 comparative conditions per model):
    - `companies_house` (`finance/uk_companies_house_handler`): 4 tiers (Single Lookup, Multi-Step Chain, Hierarchy Disambiguation, Filing Cessation Audit).
    - `office_mail` (`comms/disposable_mailbox`): 4 tiers (Direct Inbox, Binary Asset Extraction, Governed Confirmation Gate, Adversarial Phishing Neutralization).
    - `wallet_screening` (`finance/wallet_screening`): 4 tiers (OFAC Sanctions Lookup, Clean History & Risk Rating, Invalid Address Format Traversal, Governed Legal Disclaimer Gate).
    - `prompt_firewall` (`security/prompt_injection_firewall`): 4 tiers (Plaintext System Prompt Override, Invisible Zero-Width Unicode Smuggling, Leetspeak / ROT13 Adversarial Bypass, Precision Threat Sanitization).
- **Universal OpenRouter Adapter Hardening (`skillware_bench/core/adapters/openrouter_adapter.py`)**:
  - Recursive BNF grammar sanitizer (`_sanitize_tool_schema`) simplifying nested array schemas to prevent grammar blowouts on vLLM backends.
  - Chat template collision resolution (`_sanitize_messages`) automatically merging system directives into the initial user turn when tools are active for Llama architectures.
  - Resilient refusal extraction capturing explicit provider refusal payloads when message content is blank.
- **Comprehensive Documentation Suite**:
  - `docs/results/overview.md`: Complete cross-model standings and capability tier breakdowns.
  - `docs/results/frontiers_vs_small.md`: Small Models + Skillware vs. Frontier LLMs Alone deep-dive.
  - `docs/results/behavioral_contracts.md`: Base64 MIME attachment traps, confirmation gating, and error modes.
  - `docs/results/token_economics.md`: Token economics, retry context bloat, and the 464 workspace scripts eliminated.
  - `docs/results/models/`: 23 dedicated model cards with 16-layer breakdown tables and AURA receipts.
- **Zero-Emoji Hygiene Compliance**: All repository files verified by `test_zero_emojis_in_tracked_files` with 100% pass rate across 70 tests.

### Changed

- **Skillware Runtime Base URL Configuration**: Patched `finance/uk_companies_house_handler` to support runtime base URL overrides via `COMPANIES_HOUSE_BASE_URL` and `COMPANIES_HOUSE_DOCUMENT_API_BASE` for offline hermetic testing.
- **Skill Context Optimization**: Tuned Skillware prompt injection to `brief` mode (236 characters) to eliminate redundant token bloat while preserving exact JSON function schema definitions.
- **Version Bump**: Bumped core package version to `0.3.0`.


## [0.2.0] - 2026-10-17

### Added

- **Frontier Sweeps, Public Leaderboard & Release Readiness (Phase 6)**:
  - Complete 7-crucible evaluation suite with empirical benchmark results across Claude Sonnet 5, Claude 3.7 Sonnet, Gemini 3.8 Pro, Gemini 3.8 Flash, GPT-5, GPT-4o, Mistral Large 3, and Ollama Llama 3.3/3.2.
  - Frontier model adapter resolution and pricing matrix for Claude Sonnet 5, Gemini 3.8, GPT-5, and Mistral Large 3.
  - Standalone SVG publication figures: `docs/figures/radar_profile.svg` and `docs/figures/empirical_lift_delta.svg`.
  - Exported production HTML dashboard: `docs/dashboard.html` and root `docs/index.html` for GitHub Pages.
  - Interactive pastel splash banner and dispatch menu: `skillware-bench menu`.
  - Added CLI `perturb` command for dynamic anti-contamination task generation with reproducible random seeds.
  - Added CLI `new-model` command for instant Bring-Your-Own-Model (BYOM) adapter scaffolding.
  - Added CLI `audit` command for deep step-by-step AURA causal provenance inspection.
  - Added GitHub Actions CI/CD workflows: full matrix testing across Python 3.10, 3.11, 3.12, 3.13, flake8 linting, black formatting checks, CLI smoke tests, and wheel packaging smoke tests (`.github/workflows/ci.yml`).
  - Added GitHub Actions PyPI trusted publishing workflow (`.github/workflows/publish.yml`).
  - Added GitHub Issue templates: `crucible_proposal.md`, `model_adapter_request.md`, `metric_rfc.md`, and `bug_report.md`.
  - Added hygiene test `test_zero_emojis_in_tracked_files` permanently banning emojis across tracked files.
  - Expanded `docs/methodology.md` with complete 10-Pillar evaluation matrix, AURA causal DAG provenance, and anti-contamination statistics.

### Fixed

- **Hermetic Infrastructure Unit Tests**: Made `CompaniesHouseClient` and `WalletScreeningClient` tests resilient by explicitly evaluating mock snapshots and ignoring placeholder local `.env` keys.
- **Windows CP1252 Terminal Encoding**: Replaced Unicode delta symbol (`\u0394`) with plain ASCII labels in terminal summary tables to prevent `charmap` codec crashes on default Windows environments.
- **BYOM Adapter Import Compatibility**: Added `skillware_bench.core.adapters.registry` re-export module so both direct and submodule imports of `AdapterRegistry` succeed.
- **Root Package Exports**: Re-exported all primary benchmark, provenance, evaluator, and dashboard classes directly from `skillware_bench`.
- **CI Linting Dependencies**: Added `flake8` and `build` to `[project.optional-dependencies] dev` in `pyproject.toml` and invoked via `python -m flake8` in CI workflows.


## [0.1.0] - 2026-10-13


### Added

- **Interactive Dashboard & Developer UX (Phase 5)**:
  - `DashboardGenerator`: Zero-dependency, single-file HTML interactive visualizer embedding 10-pillar spider charts, delta optimization plots, and crucible execution matrices.
  - CLI `dashboard` Command: Added `skillware-bench dashboard [--suite <name>] [--output <path>] [--open-browser]` for one-command visual inspection.
  - BYOM Example Script: Added `examples/eval_custom_model.py` demonstrating Bring-Your-Own-Model integration in 20 lines of code.
  - Hermetic Docker Environment: Added production-grade `Dockerfile` with non-root security boundaries for reproducible containerized evaluation runs.

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
