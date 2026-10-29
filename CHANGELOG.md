# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- **Companies House Skillware arm failed on standard installs (`scripts/run_tiered_ablation_bench.py`)**:
  - **Impact**: Users who installed from a clean clone (`pip install -e .`, which pulls `skillware` from PyPI) saw the Skillware arm fail all four Companies House tiers. Vanilla and the other scenarios were unaffected.
  - **Cause**: The script assumed the Companies House skill reads `COMPANIES_HOUSE_BASE_URL` to reach the hermetic mock server. Released `skillware` (0.6.0) instead uses the official API URL, set when the module is imported. So the skill called the live API with a mock key and got HTTP 401. Maintainer runs did not show this, because the script prepended a local, unreleased `skillware/` checkout that does read the variable.
  - **Fix (bench only, no changes to Skillware)**: Added `skillware_bench/infra/skill_routing.py` (`bind_skill_to_mock`). After loading the skill, the bench points its base URL and HTTP layer at the mock server. The local `skillware/` checkout is now only prepended when it exists.
  - **Result**: Companies House tiers run against the mock server whether `skillware` comes from PyPI, an editable install, or a local checkout. Covered by `tests/bench/test_skill_routing.py`.
  - The end-of-run output now states that the ablation report carries a SHA-256 integrity seal, and that full AURA traces with Ed25519 receipts come from `skillware-bench run --live`.
  - Reported by Martin Rizzo Lozano.

## [0.3.3] - 2026-10-28

### Added

- **Publication Figures in Root Documentation (`README.md`)**:
  - Embedded **Figure 14** (*Run-to-Run Determinism & Variance Contraction* across 40 seeded replays under identical prompts).
  - Embedded **Figure 18** (*Equip-Any-Model Pass Rate Uplift Trajectories* demonstrating sovereign model capability leap).
  - Embedded **Figure 20** (*Token Ledger Breakdown per Tool Call* on Office Mail attachment extraction, detailing -70.6% token tax excision).
  - Embedded **Figure 33** (*368-Layer Benchmark Call Survival Flow* showing 94.1% clean first-pass calls under Skillware vs 71.2% in Vanilla).
- **Standardized Shields.io Zenodo Concept DOI Badge**:
  - Replaced third-party dynamic badge with standard flat-square shields.io badge (`DOI-10.5281/zenodo.23725543-007ec6`) matching the repository's pastel design system.
  - Linked permanent Zenodo Concept DOI (`https://doi.org/10.5281/zenodo.23725543`) across `README.md`, `CITATION.cff`, and `pyproject.toml`.
- **Grounded Framework Specification**:
  - Aligned Skillware section in `README.md` with the 5-layer skill bundle anatomy (`Contract`, `Effect`, `Directive`, `Assurance`, `Interface`) and the motto *Decoupling capability from intelligence*.

## [0.3.2] - 2026-10-28

### Added

- **Zero-Cost CLI Report Verification (`skillware-bench verify`)**:
  - Enhanced `skillware_bench/cli.py` and `skillware_bench/core/provenance.py` (`ProvenanceEngine.verify_report`) to support independent cryptographic verification of `.json` benchmark reports in addition to `.jsonl` AURA traces.
  - Recomputes the canonical JSON payload SHA-256 digest in sub-second host time without invoking external APIs, spending tokens, or relying on network access.
  - Added comprehensive verification unit tests in `tests/bench/test_provenance.py` validating authentic reports, catching corrupted payloads, and detecting tampered verdicts.
- **Tracked Canonical 23-Model Execution Reports (`benchmarks/reports/`)**:
  - Published and tracked all 23 canonical 16-layer benchmark execution reports directly in Git, recording complete experimental telemetry across 736 live conditions (turn counts, token consumption, execution latencies, disk/state diffs, verdicts, and anchored AURA SHA-256 receipts).
  - Created `benchmarks/reports/README.md` featuring:
    - Master Receipts & Attestation Index cataloging all 23 models, report files, run IDs, and SHA-256 digests.
    - Deep-dive into AURA Harness provenance, the live causal AuditSpine, and sealed session deliverables.
    - Explanation of the SHA-256 cryptographic avalanche effect illustrating why altering verdicts, token counts, or latencies invalidates receipts.
    - CLI verification command instructions and terminal output examples.
- **Full 23-Model Master Standings Table (`docs/leaderboard.md`)**:
  - Expanded `docs/leaderboard.md` to include the complete 23-model standings table (ranking pass rates, token reduction percentages, speedups, and code debugging overhead eliminated) alongside the representative 8-model exhibit.
- **Model Card Attestation Links**:
  - Cross-referenced all 23 individual model cards (`docs/results/models/*.md`) with direct links to their canonical report JSON in `benchmarks/reports/` and reproducible `skillware-bench verify` invocation commands.
- **Contributing Protocols for Autonomous Logical Systems (`CONTRIBUTING.md`)**:
  - Authored explicit contribution guidelines tailored for both human researchers and autonomous logical systems / AI agents.
  - Established Skillware (`arpahls/skillware`) as the foundational, non-negotiable evaluation axis.
  - Strictly prohibited "markdown skills" (prompt-only pseudo-skills or unstructured markdown instructions) in favor of authentic, typed, schema-validated Skillware skills.
  - Detailed five actionable contribution pathways to elevate future benchmark runs (simulation crucibles meeting the Five Invariants, sovereign model adapters, tiered ablation scaling, AURA attestation, and verified report submissions).
- **Pastel Ecosystem Badging & README Polish (`README.md`)**:
  - Added minimal, soft light pastel badges matching `arpahls/skillware`:
    - Skillware 0.6.0 (`#D4E4F1`, pastel blue)
    - License MIT (`#efcefa`, pastel lavender)
    - Python 3.10+ (`#bae6fd`, pastel sky)
    - CI passing (`#bbf7d0`, pastel mint)
    - Attestation AURA (`#ffdac1`, pastel peach)
  - Added quick-navigation jump links, CLI quickstart reproduction commands, and formal BibTeX citing block.
- **GitHub Workflow & Contribution Template Hardening (`.github/`)**:
  - Enhanced `.github/workflows/ci.yml` to automatically audit markdown links/images and run `skillware-bench verify` across all matrix Python versions (3.10-3.13) and clean virtualenv wheel smoke runs.
  - Overhauled `.github/PULL_REQUEST_TEMPLATE.md` to enforce the Zero-Hotfix Preflight Checklist, Ripple Effects Matrix verification, authentic Skillware checks, and AURA cryptographic receipt validation.
  - Aligned `.github/ISSUE_TEMPLATE/` (`crucible_proposal.md`, `model_adapter_request.md`) with the Five Crucible Invariants and capability tier standards; added dedicated `benchmark_report_submission.md` issue template for external empirical report contributions.

### Changed

- **Core Dependency Version Alignment (`pyproject.toml`)**:
  - Updated minimum dependency constraints to `skillware>=0.6.0` and `aura-harness>=0.3.6` reflecting published PyPI releases.
- **AURA Harness Provenance Grounding**:
  - Grounded all attestation documentation across `benchmarks/reports/README.md`, `docs/methodology.md`, and `docs/results/latency_and_auditability.md` strictly in AURA Harness (`αύρα` — AVRA / AURA, PyPI: `aura-harness`) architecture: runtime coat around the agent body cavity, egress policy boundary, live causal AuditSpine (`AuraEvent`), sealed session exports, and SHA-256 receipts.
- **Hygiene Test Configuration (`tests/hygiene/test_repo_hygiene.py`)**:
  - Updated `test_zero_emojis_in_tracked_files` to exclude `benchmarks/reports/*.json` so empirical frontier model completions containing literal response symbols are preserved verbatim, while maintaining strict zero-emoji enforcement across all code, tests, scripts, and documentation markdown.

### Removed

- **Legacy & Obsolete Artifacts**:
  - Purged obsolete legacy SVG figures and deprecated `export_figures` runner methods to maintain a clean, publication-grade repository tree.

## [0.3.1] - 2026-10-27

### Added

- **Publication Exhibit Suite (46 Active High-Resolution Exhibits)**:
  - Exported all 46 active publication-grade exhibits from `scratch/figuregen/clean htmls/` as 3x device-pixel-ratio (Retina / 300 DPI, 2520px–2700px) PNGs into `docs/figures/`.
  - Created `docs/figures/manifest.json` cataloging each exhibit's metadata, titles, clean authoritative captions, and file sizes.
  - Documented 19 deferred exhibits reserved for specialized ablation extensions in `docs/exhibits.md`.
  - Added `docs/exhibits.md` featuring the complete gallery and taxonomy across 6 publication themes.
- **Latency, Concurrency & Cryptographic Audit Deep-Dive (`docs/results/latency_and_auditability.md`)**:
  - Authored comprehensive deep-dive detailing the Four-Scale Continuum (>24,000x dynamic range), concurrency scaling up to 512 workers (sustaining 16.9 vs 5.0 tasks/min), tail latency compression (45.4% drop at P99), and AURA AuditSpine cryptographic verification latency (<0.50 ms, <0.01% runtime overhead).
- **Public Leaderboard Standings (`docs/leaderboard.md`)**:
  - Integrated representative 8-model standing matrix (`tab04_eight_model_leaderboard.png`) and equip-any-model uplift trajectories (`fig18_equip_any_model_uplift.png`).
- **Comprehensive Documentation Grounding & Visual Embeds**:
  - `README.md`: Embedded key figures (`fig25_capability_compression_heatmap.png`, `tab07_four_axis_summary.png`, `fig12_cost_capability_frontier.png`, `fig11_latency_anatomy.png`) with authoritative captions.
  - `docs/results/overview.md`: Embedded `tab07_four_axis_summary.png`, `fig25_capability_compression_heatmap.png`, and `fig13_gain_by_task_family.png`.
  - `docs/results/frontiers_vs_small.md`: Replaced visual placeholder with `fig05_parameter_paradox.png` and `fig18_equip_any_model_uplift.png`.
  - `docs/results/token_economics.md`: Replaced visual placeholder with `fig04_cost_cascade.png`, `fig20_token_ledger_per_call.png`, and `fig47_completion_bloat_ratio.png`.
  - `docs/results/behavioral_contracts.md`: Replaced visual placeholder with `fig06_context_excision.png`, `fig07_wallet_gate.png`, and `fig33_call_survival_flow.png`.
  - `docs/methodology.md`: Embedded `fig21_measurement_harness.png`, `fig02_bundle_anatomy.png`, and `tab03_progressive_difficulty_tiers.png`.
  - `docs/crucibles.md`: Embedded `tab01_ecosystem_taxonomy.png`, `tab02_three_stage_firewall.png`, and `fig28_kill_chain_coverage.png`.

### Changed

- **Capability Tier Standardization**:
  - Standardized all 23 model cards (`docs/results/models/*.md`), overview tables, and leaderboard docs to use the 4 canonical locked capability tiers: `Frontier`, `Enterprise`, `Compact`, and `Edge`, eliminating ad-hoc parameter guesswork.
- **Repository Documentation Sitemap**:
  - Synchronized sitemaps across `README.md` and `docs/README.md` to link all new analyses, exhibits catalog, and leaderboard.


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
