# Contributing to Skillware-Bench

Welcome to Skillware-Bench. We are building the open, transparent, empirical benchmark suite and evaluation harness for Skillware skills, agent constitutions, and frontier language models.

Whether you are a human researcher, a systems engineer, or an autonomous logical system (AI agent, reasoning model, or automated evaluation pipeline), this guide serves as the definitive protocol for contributing to the benchmark. Follow this guide precisely to ensure your contributions pass all continuous integration gates on the first attempt without requiring follow-up hotfixes.

---

## Navigation

| Section | Description |
| :--- | :--- |
| [Skillware as the Foundational Evaluation Axis](#skillware-as-the-foundational-evaluation-axis) | Core philosophy and strict prohibition of markdown pseudo-skills |
| [Protocols for Autonomous Logical Systems & AI Agents](#protocols-for-autonomous-logical-systems--ai-agents) | Inviolable machine invariants for AI coding systems |
| [The Ripple Effects Matrix](#the-ripple-effects-matrix-what-to-update-when-changing-x) | Cross-cutting file dependencies that break CI if missed |
| [How to Make the Next Benchmark Run Better (v0.4.0+)](#how-to-make-the-next-benchmark-run-better-v040) | Five contribution tracks for expanding benchmark coverage |
| [The Five Crucible Invariants](#the-five-crucible-invariants) | Mandatory architectural rules for evaluation crucibles |
| [Getting Started](#getting-started) | Environment setup, dependencies, and local installation |
| [Repository Anti-Patterns (What to Avoid)](#repository-anti-patterns-what-to-avoid) | Traps that lead to rejected pull requests or hotfixes |
| [The Zero-Hotfix Preflight Checklist](#the-zero-hotfix-preflight-checklist) | Complete, sequential commands to run before opening a PR |
| [Responsible Disclosure & Security](#responsible-disclosure--security) | Reporting security vulnerabilities and sandboxing adversarial tests |
| [Legal Notice and Code Ownership](#legal-notice-and-code-ownership) | MIT licensing and inbound intellectual property terms |

---

## Skillware as the Foundational Evaluation Axis

Skillware-Bench exists to measure a fundamental transition in agent architecture: moving from unconditioned, unguided code synthesis to governed, typed, deterministic skill execution.

### The Primary Evaluation Axis: Governed Skillware Execution
The central scientific axis of this repository is [Skillware](https://github.com/arpahls/skillware) (`arpahls/skillware`). Every crucible evaluates the delta between:
1. **Vanilla Baseline**: The model receives raw agent primitives (`execute_python` and `http_request`). It must discover endpoints, write complete scripts, interpret stdout/stderr, debug runtime exceptions across multiple turns, and absorb true context expansion costs.
2. **Skillware Equipped**: The model receives authentic, typed Skillware skill bundles. Invocations execute through deterministic JIT handlers, validate parameter schemas, enforce constitutional boundaries, and operate under [AURA Harness](https://github.com/arpahls/aura) runtime coats.

### Zero Tolerance for "Markdown Skills" or Ad-Hoc Scripts
Skillware-Bench strictly prohibits "markdown skills" (md skills / prompt-only pseudo-skills) as evaluated tools:
- **What is a "Markdown Skill"?** Unstructured natural language instructions, copy-pasted prompt wrappers, or raw markdown documentation dumped into a model's system prompt to simulate a tool without code or schema.
- **Why They Are Prohibited**: Markdown-only pseudo-skills inflate prompt context, trigger non-deterministic hallucinations, lack physical argument validation, and cannot be cryptographically verified or gated at runtime. They defeat the entire purpose of rigorous agent governance.
- **The Invariant**: All skills evaluated in Skillware-Bench must be authentic, typed Skillware skills possessing declarative JSON/OpenAPI schemas, typed parameter contracts, deterministic Python handlers, and explicit capability boundaries.

---

## Protocols for Autonomous Logical Systems & AI Agents

Skillware-Bench is designed for collaboration between human engineers and autonomous logical systems. When an autonomous agent or reasoning system contributes to this repository, it must adhere to the following machine invariants:

1. **Strict Zero-Emoji Invariant**:
   - Zero emojis are permitted anywhere in the repository: not in code, docstrings, commit messages, CLI outputs, test assertions, or markdown documentation.
   - Every file change is mechanically audited by `tests/hygiene/test_repo_hygiene.py::test_zero_emojis_in_tracked_files`. Even a single emoji will cause CI to fail immediately.
2. **Mandatory SPDX License Headers**:
   - Every Python file must start with valid SPDX headers within lines 1 to 5:
     ```python
     # Copyright (c) 2026 ARPA Hellenic Logical Systems
     # SPDX-License-Identifier: MIT
     ```
   - Checked by `tests/hygiene/test_spdx_headers.py::test_package_source_spdx_headers`.
3. **Cryptographic Grounding & Tamper-Evidence**:
   - Never forge, edit, or backdate cryptographic SHA-256 receipts or AURA traces.
   - Any modification to empirical run outputs must be produced by running authentic benchmark executions or test-suite verifications.
4. **Hermetic Isolation**:
   - Never touch or commit `.env` files, live credentials, or unmasked tokens.
   - Ephemeral mock servers must dynamically bind to Port 0 (`127.0.0.1:0`) to eliminate cross-process socket collisions.
5. **Local Preflight Verification**:
   - Autonomous systems must run `pytest tests/ -v`, `black --check .`, and `flake8` to guarantee clean exit codes before submitting pull requests.

---

## The Ripple Effects Matrix (What to Update When Changing X)

To prevent broken builds, test regressions, or follow-up hotfixes, consult this matrix whenever modifying code in Skillware-Bench. Changing one component frequently requires synchronized updates in other files:

| If You Change / Add... | You Must Also Update / Verify... | Why / Failure Mode if Missed |
| :--- | :--- | :--- |
| **New Crucible Class** (`skillware_bench/suites/<name>.py`) | 1. Declarative YAML: `benchmarks/scenarios/<id>.yaml`<br/>2. Registration: `skillware_bench/suites/__init__.py` in `ALL_CRUCIBLES`<br/>3. Mock server: `skillware_bench/core/hermetic_mock_server.py`<br/>4. Tests: `tests/bench/test_crucibles.py` and `test_live_crucibles.py`<br/>5. Documentation: `docs/crucibles.md` | `test_all_crucibles_registered` fails if not in `ALL_CRUCIBLES`. `skillware-bench list` omits the crucible. CI fails if mock mode cannot run offline without keys. |
| **New Model Adapter** (`skillware_bench/core/adapters/<name>.py`) | 1. Registration: `skillware_bench/core/adapters/__init__.py` via `AdapterRegistry.register()`<br/>2. Dependencies: `pyproject.toml` under `[project.optional-dependencies]` and `all`<br/>3. Unit Tests: `tests/bench/test_adapters.py` (token usage, retry logic)<br/>4. Model Card: `docs/results/models/<name>.md` | `get_adapter()` fails at runtime. Missing dependencies cause `ModuleNotFoundError` in environments without provider extras. |
| **Benchmark Execution Report** (`benchmarks/reports/<model>.json`) | 1. Master Table: `benchmarks/reports/README.md`<br/>2. Verification Test: Run `skillware-bench verify benchmarks/reports/<model>.json`<br/>3. Model Card: Link report and verify command in `docs/results/models/<model>.md`<br/>4. Leaderboard: Update `docs/leaderboard.md` if rankings shift | `HASH_MISMATCH` exit code 1 if payload altered. Broken links in docs audited by `audit_md_links.py`. |
| **Package Exports** (`skillware_bench/__init__.py`) | 1. `__all__` list in `skillware_bench/__init__.py`<br/>2. `expected_exports` list in `tests/hygiene/test_package_integrity.py` | `test_package_exports()` fails in CI if public symbols are added or removed without updating hygiene assertions. |
| **Package Version Bump** | 1. `skillware_bench/__init__.py` (`__version__ = "X.Y.Z"`)<br/>2. `pyproject.toml` (`version = "X.Y.Z"`)<br/>3. `CITATION.cff` (`version: X.Y.Z` and `date-released: YYYY-MM-DD`)<br/>4. `CHANGELOG.md` (new version header) | `test_version_consistency()` fails if `__version__` and `pyproject.toml` differ. `test_citation_cff_metadata()` fails if CITATION.cff is desynchronized. |
| **CLI Arguments / Commands** (`skillware_bench/cli.py`) | 1. Tests: `tests/bench/test_cli.py`<br/>2. Documentation: `README.md` and `docs/README.md`<br/>3. Shell completion / help text | `test_cli_*` fails if command signatures change. Broken documentation links or missing arguments confuse users. |
| **Documentation & Markdown Files** (`docs/`, `*.md`) | 1. Link audit: `python scripts/audit_md_links.py`<br/>2. Zero emojis: No symbols, thumbs, or icon characters in prose<br/>3. Formatting: Standard markdown tables and GitHub-flavored markdown | CI link audit fails if relative links or image paths are broken. Zero-emoji test fails on unicode symbols. |

---

## How to Make the Next Benchmark Run Better (v0.4.0+)

We actively solicit contributions that expand the breadth, robustness, and adversarial rigor of upcoming fleet benchmark runs:

### Track 1: Propose Realistic Simulation Crucibles
The benchmark evaluates models across real-world, high-stakes operational environments. We welcome new crucibles reflecting enterprise workflows (e.g., regulatory compliance, automated reconciliation, multi-system orchestration, cloud infrastructure mutation). Every crucible must satisfy [The Five Crucible Invariants](#the-five-crucible-invariants).

### Track 2: Implement Frontier & Sovereign Model Adapters
Skillware-Bench evaluates a diverse roster of frontier commercial APIs and local open-weight sovereign models:
- Subclass `BaseModelAdapter` in `skillware_bench/core/adapters/`.
- Accurately capture `prompt_tokens`, `completion_tokens`, and `cached_tokens` directly from provider metadata.
- Record execution latency per turn.
- Wrap remote calls in `execute_with_retry` to handle rate limits (HTTP 429) and server drops (HTTP 500/503).
- Register new adapters using `AdapterRegistry.register("provider/model-prefix", AdapterClass)`.
- Never spoon-feed high-level parsing utilities to Vanilla baselines. They receive only raw agent primitives (`execute_python` and `http_request`).

### Track 3: Expand the Tiered Ablation Matrix
The benchmark standardizes on a 16-layer progressive matrix (4 crucibles × 4 difficulty tiers):
- **Tier 1 (Single Lookup)**: Direct parameter extraction and single-step API dispatch.
- **Tier 2 (Dependent Chain)**: Multi-step workflows requiring sequential state propagation.
- **Tier 3 (Disambiguation & Hierarchy)**: Navigating organizational trees, conflicting names, and active vs. dissolved entities.
- **Tier 4 (Adversarial Injection & Boundary Stress)**: Neutralizing prompt injection payloads and respecting irreversible confirmation boundaries.

Contributors can propose **Tier 5+ advanced crucibles** focusing on multi-agent consensus, long-context drift across 50+ turns, and automated rollback under unexpected API faults.

### Track 4: Causal Provenance & Attestation via AURA Harness
Skillware-Bench integrates [AURA Harness](https://github.com/arpahls/aura) (`aura-harness`, Greek: *αύρα* / *AVRA*) as its attestation coat:
- Ensure all execution turns, schema checks, tool dispatches, and environment state diffs emit structured `AuraEvent` records to the live AuditSpine.
- Verify that every benchmark trial concludes with a sealed session export and an immutable SHA-256 cryptographic receipt (`aura_cryptographic_receipt`).
- Maintain sub-millisecond host overhead (<50 µs per turn) to keep attestation costs under 0.01% of total runtime.

### Track 5: Submit Verified Benchmark Execution Reports
Researchers and organizations evaluating models can contribute empirical reports to [`benchmarks/reports/`](benchmarks/reports/README.md):
1. Execute the full 16-layer benchmark using `scripts/run_tiered_ablation_bench.py`.
2. Ensure the resulting report JSON is sealed with an AURA cryptographic receipt.
3. Validate the report locally using the CLI:
   ```bash
   skillware-bench verify benchmarks/reports/<model_id>.json
   ```
4. Submit the verified report and updated model card (`docs/results/models/<model_id>.md`) in a pull request.

---

## The Five Crucible Invariants

Every simulation crucible submitted to Skillware-Bench must satisfy these five mandatory architectural invariants:

1. **Dual-Engine Execution**:
   - Must provide deterministic `--mock` execution for sub-second, zero-cost CI testing without requiring API credentials.
   - Must provide `--live` execution against live frontier endpoints or local sovereign inference servers.
2. **Negative Controls Mandate**:
   - Every crucible evaluating safety boundaries, confirmation gates, or schema validation must include an explicit negative control. If a scenario passes when safety constraints are stripped, the crucible is invalid because it lacks measurement sensitivity.
3. **Ambiguous Consent Resistance**:
   - Scenarios involving critical side effects (sending email, executing wire transfers, deleting records) must test user inputs that are ambiguous, partial, or hesitant (e.g., *"looks fine, but make sure the subject says urgent"*). Agents must never treat ambiguous replies as explicit confirmation (`confirmed: true`).
4. **Multi-Vector State Diff Verification**:
   - Never evaluate models by searching for regex strings in model prose. Evaluations must measure ground-truth environmental state diffs: files written to disk, staged drafts, sent messages, and API status codes.
5. **Hermetic Port 0 Simulation**:
   - Mock servers must run locally and offline, simulating REST endpoints, mailboxes, and corporate registries dynamically binding to ephemeral Port 0 (`127.0.0.1:0`) to eliminate cross-process socket collisions.

---

## Getting Started

### 1. Fork and Clone
Fork [ARPAHLS/skillware-bench](https://github.com/ARPAHLS/skillware-bench) to your GitHub account, then clone locally:

```bash
git clone https://github.com/<your-username>/skillware-bench.git
cd skillware-bench
git remote add upstream https://github.com/ARPAHLS/skillware-bench.git
```

### 2. Set Up Virtual Environment
Requires **Python 3.10+**:

```bash
# Windows:
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate

# Install in editable mode with development and provider dependencies:
pip install -e ".[dev,all]"
```

---

## Repository Anti-Patterns (What to Avoid)

To ensure your pull request merges cleanly without follow-up hotfixes, avoid these known repository anti-patterns:

- **No Emojis Anywhere**: Never introduce unicode emojis in code, commits, docstrings, or markdown documentation.
- **No Markdown Pseudo-Skills**: Never submit prompt-only markdown pseudo-skills as evaluated tools. Skills must be typed Skillware skills.
- **No Spoon-Fed Baseline Utilities**: Never equip Vanilla baselines with pre-parsed domain tools. Baselines must run raw `execute_python` and `http_request` to measure true code generation and debugging economics.
- **No Regex Scrapers for Verdicts**: Evaluators must check structured environmental state diffs, never regex matches on conversational prose.
- **No Hardcoded Network Ports**: Never bind mock servers or tests to static ports (e.g. `8080`, `5000`). Always bind to `127.0.0.1:0`.
- **No Hardcoded Credentials or Leaked Files**: Never commit `.env` files, temporary run outputs, or untracked reference folders (`skillware/`, `aura/`, `mnemolink/`).
- **No Silent Constraint Bypasses**: When a model violates a constitutional boundary, log an explicit violation rather than silently ignoring it.
- **No Desynchronized Version Numbers**: Never bump version in `pyproject.toml` without simultaneously updating `skillware_bench/__init__.py` and `CITATION.cff`.
- **No Ad-Hoc File Paths**: Always use `pathlib.Path` for platform-independent filesystem operations across Windows, macOS, and Linux.

---

## The Zero-Hotfix Preflight Checklist

Before pushing commits or opening a pull request, execute this sequential verification checklist locally. If all six steps pass with exit code 0, your pull request is guaranteed to pass CI:

```bash
# Step 1: Code Formatting (Black, line-length 100)
python -m black --check .

# Step 2: Linter Hygiene (Flake8, zero warnings)
python -m flake8 . --count --statistics

# Step 3: Complete Test Suite (Unit, integration, and live crucibles)
pytest tests/ -v

# Step 4: Dedicated Hygiene & Packaging Invariants
pytest tests/hygiene/ -v

# Step 5: Markdown Links and Image Embed Integrity Audit
python scripts/audit_md_links.py

# Step 6: CLI Smoke Test (Environment, registry, and mock execution)
skillware-bench check-env
skillware-bench list
skillware-bench run --mock
```

Check your git working tree to ensure no untracked artifacts or secrets are left behind:

```bash
git status
```

---

## Responsible Disclosure & Security

Skillware-Bench evaluates mission-critical agent safety, prompt injection resistance, and boundary enforcement:
- If you discover a security vulnerability in the harness or evaluation crucibles, do NOT open a public issue.
- Report all vulnerabilities privately to [security@arpacorp.net](mailto:security@arpacorp.net) in accordance with our [Security Policy](SECURITY.md).
- Adversarial simulation fixtures must remain strictly sandboxed or use hermetic offline mock registries.

---

## Legal Notice and Code Ownership

By contributing to Skillware-Bench, you agree that:
1. Your contributions are licensed under the project's [MIT License](LICENSE).
2. You certify that you are the original author of the contribution or have the requisite rights and permissions to submit the work under the MIT License.
3. Inbound contributions do not infringe upon any third-party intellectual property rights or trade secrets.
