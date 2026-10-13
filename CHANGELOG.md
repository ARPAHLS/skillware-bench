# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-10-13

### Added

- **Core Benchmark Architecture & Harness Engine**:
  - Initial scaffolding for the Skillware-native empirical benchmark suite.
  - Multi-tier progression framework: Tier 1 (Deterministic Mocked Skills), Tier 2 (Tool-Selection & Schema Validity), Tier 3 (Constitutional Safety & Procedural Compliance), Tier 4 (Multi-Skill Pipeline Chaining), and Tier 5 (Model Economics: Cost, Latency, & Token Bloat).
  - A/B Comparative Crucible Engine: With-Skillware vs Without-Skillware (Generic Prompt) delta evaluation.
- **Initial Real-World Simulation Crucibles**:
  - `Crucible 1: Gmail Workflow (office/gmail_handler)`: End-to-end recipient resolution, inbox search, preview-before-send gating, ambiguous consent resistance, and inbound prompt-injection defense.
  - `Crucible 2: UK Companies House (finance/uk_companies_house_handler)`: Deterministic entity search, officer/PSC extraction, filing history navigation, and anti-hallucination company number checks.
  - `Crucible 3: Crypto Wallet Screening (finance/wallet_screening)`: Sanctions checks (OFAC), mixer address screening, risk scoring, and non-legal advice disclaimer compliance.
  - `Crucible 4: Constitutional Safety & Boundary Gates`: Negative controls, unauthorized send blocking, `dry_run` enforcement, and prompt injection firewall resilience.
  - `Crucible 5: Chained Compliance Pipeline`: Multi-step extraction (`pii_masker` → `uk_companies_house_handler` → `token_limiter`).
- **Frontier & Sovereign Model Adapters**:
  - Universal runner supporting Google Gemini (`gemini-2.5-pro`, `gemini-2.5-flash`), Anthropic Claude (`claude-3-7-sonnet`, `claude-3-5-haiku`), OpenAI (`gpt-4o`, `o3-mini`), Mistral AI (`mistral-large`, `codestral`), DeepSeek, Groq, and local Ollama (`llama3.2`, `qwen2.5`).
- **Metrics & Reporting Engine**:
  - 6-pillar evaluation metric: Schema Accuracy, Procedural Sequence, Constitutional Compliance, Token Compression ($\Delta$), Latency Acceleration ($\Delta$), and Actionability.
  - CLI commands: `skillware-bench run`, `skillware-bench list`, `skillware-bench compare`, and `skillware-bench report`.
  - Machine-readable JSON output and rich terminal tabular summaries.
- **Repository Baseline & Brand Alignment**:
  - Standardized ARPA Hellenic Logical Systems branding, pastel badge styling, `CITATION.cff`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and MIT License.
