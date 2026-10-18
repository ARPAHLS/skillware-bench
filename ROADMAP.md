# Skillware-Bench: Architectural Diary and Strategic Roadmap

This document serves as the project diary, lessons-learned repository, and strategic roadmap. It ensures the team maintains continuity, avoids repeating past architectural mistakes, and drives toward the ultimate benchmark North Star.

---

## 1. The North Star (Winning Flag)

The primary mission of **Skillware-Bench** is to establish the industry-standard, reproducible, and verifiable empirical proof that **Skillware skill bundles** transform autonomous AI agents from costly, fragile, trial-and-error code executioners into deterministic, high-speed, cost-effective, and constitutionally secure operators.

### Quantitative Winning Targets

1. **Token Economy**: >= 60% total token reduction across multi-turn, multi-step workflows.
2. **Cost Efficiency**: >= 50% cost reduction by eliminating multi-turn script debugging and token blowout.
3. **Execution Latency**: >= 2.0x wall-clock latency speedup by replacing iterative error analysis with deterministic single-turn tool calls.
4. **Deterministic Security**: 100% resistance to indirect prompt injection and strict physical environment safety gating (e.g. 403 Forbidden on unconfirmed side-effects).
5. **Full Forensic Reproducibility**: 100% air-gapped workspaces with script diff histories (`diff_k_to_k+1.patch`) and cryptographic AURA SHA-256 trace verification.

---

## 2. Engineering Diary & Lessons Learned (Mistakes Avoided)

### Lesson 1: The Spoon-Fed Tool Fallacy (Realistic Agent Economics)
- **The Past Mistake**: In earlier benchmark designs, Vanilla baselines were given high-level, bespoke tools (e.g. a naive `search_companies` or `read_email` function). This artificially flattened the comparison: Vanilla appeared faster or cheaper simply because the domain logic had already been coded for it into the tool!
- **The Correct Architecture**: Real-world agents attempting complex tasks do not have pre-packaged domain tools. Vanilla baselines must operate with authentic agent primitives: `execute_python` and raw `http_request`. Vanilla must discover endpoints, inspect HTTP status codes, write complete Python scripts in an isolated workspace, and debug tracebacks across turns. Skillware operates via its verified, deterministic skill bundles.
- **Result**: Under realistic agent economics, Vanilla burns tens of thousands of tokens and dozens of script attempts on complex tasks, while Skillware solves them deterministically in 1 to 4 turns.

### Lesson 2: Context Bloat in System Directives
- **The Past Mistake**: When initializing `SkillContext`, using `mode="directives"` appended ~15,800 characters (~4,000 tokens) of instruction manuals to the system prompt on every single turn. This caused trivial Tier 1 tasks to consume 18,000 tokens.
- **The Correct Architecture**: Switched to `mode="brief"` (236 characters) combined with high-precision OpenAPI function schemas generated directly from skill bundles (`SkillLoader.to_openai_tool`).
- **Result**: Prompt overhead slashed by > 65% per turn, restoring natural economic advantage to Skillware across all difficulty tiers.

### Lesson 3: Hermetic Ephemeral Port Allocation (Port 0)
- **The Past Mistake**: Hardcoding mock server ports (e.g. `8080` or `5000`) caused intermittent `[Errno 98/10048] Address already in use` flakiness on CI, background subagents, or local runs.
- **The Correct Architecture**: Created `HermeticMockServer` using Python's `ThreadingHTTPServer` binding to `("127.0.0.1", 0)`. The OS dynamically allocates a free ephemeral port, accessible via `server.base_url`.
- **Result**: Zero port collision flakiness, instant startup and shutdown, and hermetic offline test runs with zero internet dependency.

### Lesson 4: Subprocess Path Resolution on Windows
- **The Past Mistake**: Passing `[sys.executable, str(script_file)]` when `cwd=str(workspace_dir)` caused Python on Windows to resolve the path as `cwd / script_file`, doubling the path and throwing `[Errno 2] No such file or directory`.
- **The Correct Architecture**: Resolved `workspace_dir = workspace_dir.resolve()` and passed the local script filename (`attempt_{idx}.py`) directly as a relative argument to `subprocess.run(..., cwd=str(workspace_dir))`.
- **Result**: Clean, cross-platform execution on Windows PowerShell and Linux bash without path resolution errors.

### Lesson 5: Physical Environment State Gating
- **The Past Mistake**: Verifying agent safety merely by checking if the model said "I will not send this" in its response text.
- **The Correct Architecture**: Grounded verification in physical environment state diffs. The mock server strictly returns `403 Forbidden` if `/email/send` is called with `confirmed != True`, and records previews in `staged_previews` and sends in `sent_messages`.
- **Result**: Irreversible actions are physically gated; evaluations verify both the verbal output and the underlying environment state.

---

## 3. The 4-Tier Difficulty Progression Model

Every benchmark scenario must scale across four distinct difficulty tiers:

| Tier | Objective | What Vanilla Must Do | What Skillware Does |
| :--- | :--- | :--- | :--- |
| **Tier 1: Single Lookup** | Basic entity resolution | Calls single HTTP endpoint or writes short fetch script | Dispatches 1 deterministic skill call |
| **Tier 2: Dependent Chain** | Multi-step dependency & binary assets | Discovers multiple endpoints, writes script to stream binary data to disk | Sequences multi-action pipeline via skill parameters |
| **Tier 3: Disambiguation** | Hierarchy, entity traps & safety gates | Probes endpoints, navigates name collisions, encounters 403 Forbidden gates | Uses verified domain taxonomy and governed preview/confirm flow |
| **Tier 4: Adversarial Defense** | Indirect prompt injection & threat defense | Must resist malicious prompt injections embedded in retrieved data | Neutralizes exfiltration vectors and reports structured security taxonomy |

---

## 4. Strategic Milestone Roadmap

### Phase 1: Hermetic Mock Engine & Synthetic Datasets [COMPLETED]
- [x] Implemented `HermeticMockServer` on dynamic Port 0.
- [x] Created `MOCK_COMPANIES_REGISTRY` with 10 UK corporate archetypes.
- [x] Created `MOCK_INBOX_REGISTRY` with 20 operational and adversarial messages.
- [x] Built unit test suite `tests/bench/test_hermetic_mock_server.py` (100% passing).

### Phase 2: Progressive Tiered Ablation Runner [COMPLETED]
- [x] Built `scripts/run_tiered_ablation_bench.py` with multi-tier execution.
- [x] Integrated air-gapped workspaces with diff patch archiving (`diff_k_to_k+1.patch`).
- [x] Integrated AURA SHA-256 cryptographic trace signing and receipt emission.
- [x] Flake8 100% clean, zero linter warnings.

### Phase 3: Validation on Initial Model (DeepSeek v4.1 Flash) [COMPLETED]
- [x] Evaluated UK Companies House (Tiers 1 to 4):
  - Skillware: 100% pass rate, 65% cost savings on Tier 3, 84% token savings on Tier 4 (where Vanilla failed).
- [x] Evaluated Office Mailbox (Tiers 1 to 4):
  - Skillware: 100% pass rate, 77% token savings on Tier 1, 81% token savings on Tier 2, 79% cost savings on Tier 3.
- [x] Cumulative 8-Tier Total: **67.8% Token Reduction**, **60.7% Cost Reduction**, **2.6x Speedup**, **100% vs 87.5% Pass Rate**.

### Phase 4: Cross-Model Validation & Comparative Model Evaluation [IN PROGRESS]
- [ ] Evaluate second cheap model for comparison (e.g. `meta-llama/llama-3.3-70b-instruct` or `qwen/qwen-2.5-72b-instruct`).
- [ ] Evaluate frontier models (Claude 3.7 Sonnet, GPT-4o / GPT-5, Gemini 1.5 / 2.0).
- [ ] Record comparative delta across model tiers in a consolidated benchmark matrix.

### Phase 5: Additional Skill Bundles Integration [PLANNED]
- [ ] Integrate completely offline local skills:
  - `office/pdf_form_filler`: Form field parsing and programmatic PDF generation.
  - `security/prompt_injection_firewall`: Inbound and outbound injection sanitization.
  - `crypto/wallet_screening`: Sanctions and risk screening against synthetic OFAC datasets.
- [ ] Expand synthetic fixtures for multi-modal and multi-domain workflows.

### Phase 6: Public Leaderboard & Empirical Publication [PLANNED]
- [ ] Run multi-seed iterations (N=5) with 95% confidence intervals and Pass@k metrics.
- [ ] Update `docs/leaderboard.md` and `docs/dashboard.html` with verified empirical multi-model data.
- [ ] Publish reproducible artifacts to GitHub Pages and Zenodo archive.
