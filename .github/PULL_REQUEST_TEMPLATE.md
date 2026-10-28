## Summary

<!-- Brief technical summary of what this pull request introduces or fixes -->

## Type of Change

- [ ] New benchmark simulation crucible (`benchmarks/scenarios/` + `skillware_bench/suites/`)
- [ ] Model adapter (`skillware_bench/core/adapters/`)
- [ ] Empirical benchmark execution report (`benchmarks/reports/`)
- [ ] Evaluation rubric, metric, or statistical estimator (`skillware_bench/core/evaluators.py`)
- [ ] Harness architecture / core agent loop / AURA provenance (`skillware_bench/core/`)
- [ ] Documentation / leaderboard / exhibits update (`docs/`)
- [ ] CI workflow / packaging / repository hygiene

## Zero-Hotfix Preflight Checklist

- [ ] `pytest tests/ -v` passes offline (all 71+ unit and integration tests)
- [ ] `pytest tests/hygiene/ -v` passes (version consistency, zero emojis, SPDX headers, package exports)
- [ ] `black --check .` passes (line length 100)
- [ ] `flake8 . --count --statistics` passes with 0 warnings
- [ ] `python scripts/audit_md_links.py` passes with 0 broken links and 0 broken images
- [ ] `skillware-bench check-env`, `skillware-bench list`, and `skillware-bench run --mock` execute cleanly
- [ ] Zero emojis anywhere in code, docstrings, commit messages, CLI output, or documentation markdown

## Ripple Effects Matrix Verified

- [ ] Consulted the Ripple Effects Matrix in `CONTRIBUTING.md`
- [ ] If adding a crucible: registered in `ALL_CRUCIBLES` in `skillware_bench/suites/__init__.py` and tested in `test_crucibles.py`
- [ ] If adding an adapter: registered via `AdapterRegistry.register()` and dependencies declared in `pyproject.toml`
- [ ] If bumping version: synchronized across `skillware_bench/__init__.py`, `pyproject.toml`, and `CITATION.cff`
- [ ] If modifying exports: updated `__all__` in `__init__.py` and `expected_exports` in `test_package_integrity.py`
- [ ] If submitting a report: added entry to `benchmarks/reports/README.md` and linked in model card
- [ ] Updated `CHANGELOG.md` under `[Unreleased]`

## Architectural Invariants Verified

- [ ] Authentic Skillware Skills: Evaluated skills are authentic, typed Skillware skills (no markdown pseudo-skills or unstructured prompt manuals)
- [ ] The Five Crucible Invariants: If adding a crucible, satisfied dual-engine execution, negative controls, ambiguous consent resistance, multi-vector state diffs, and Port 0 hermetic mock servers
- [ ] AURA Cryptographic Receipts: If adding reports, verified via `skillware-bench verify benchmarks/reports/<model>.json`
- [ ] Secret Isolation: No API keys, `.env` files, ephemeral run logs, or reference checkouts (`skillware/`, `aura/`, `mnemolink/`) included

## Inbound License & Original Work

- [ ] I certify that this contribution is my original work (or that I have the right to submit it) and agree to license it under the MIT License.
