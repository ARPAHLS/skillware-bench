# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Test repository hygiene, baseline documentation, and secret isolation."""

from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_gitignore_protects_references_and_secrets():
    gitignore_path = REPO_ROOT / ".gitignore"
    assert gitignore_path.exists(), ".gitignore must exist"
    content = gitignore_path.read_text(encoding="utf-8")

    assert "skillware/" in content, ".gitignore must ignore reference skillware/"
    assert "aura/" in content, ".gitignore must ignore reference aura/"
    assert "mnemolink/" in content, ".gitignore must ignore reference mnemolink/"
    assert ".env" in content, ".gitignore must ignore .env"
    assert "runs/" in content, ".gitignore must ignore ephemeral runs/"


def test_no_references_or_secrets_tracked_in_git():
    # Use git ls-files to verify tracked index
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    tracked_files = result.stdout.splitlines()

    for path in tracked_files:
        assert not path.startswith("skillware/"), f"Reference repo file tracked in git: {path}"
        assert not path.startswith("aura/"), f"Reference repo file tracked in git: {path}"
        assert not path.startswith("mnemolink/"), f"Reference repo file tracked in git: {path}"
        assert not path.startswith("runs/"), f"Ephemeral run report tracked in git: {path}"
        assert path != ".env", ".env must never be tracked in git!"


def test_baseline_docs_exist():
    required_files = [
        "LICENSE",
        "README.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        "CITATION.cff",
        "pyproject.toml",
        ".env.example",
    ]
    for fn in required_files:
        path = REPO_ROOT / fn
        assert path.exists(), f"Required baseline file {fn} is missing!"
        assert path.stat().st_size > 50, f"Baseline file {fn} is suspiciously small/empty!"


def test_citation_cff_metadata():
    citation_path = REPO_ROOT / "CITATION.cff"
    content = citation_path.read_text(encoding="utf-8")
    assert "cff-version: 1.2.0" in content
    assert "Ross Peili" in content or "Peilivanidis" in content
    assert "ARPA Hellenic Logical Systems" in content
    assert "https://github.com/arpahls/skillware-bench" in content


def test_security_policy_content():
    sec_path = REPO_ROOT / "SECURITY.md"
    content = sec_path.read_text(encoding="utf-8")
    assert "security@arpacorp.net" in content
    assert "Zero Secret Leakage" in content or "Permissive Fortress" in content


def test_zero_emojis_in_tracked_files():
    import re

    result = subprocess.run(
        ["git", "ls-files"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    emoji_pattern = re.compile(r"[\U00010000-\U0010ffff\u2600-\u27bf]")
    violations = []
    for file_rel in result.stdout.splitlines():
        if file_rel.endswith((".png", ".ico", ".jpg", ".svg")):
            continue
        full_path = REPO_ROOT / file_rel
        if not full_path.exists():
            continue
        try:
            content = full_path.read_text(encoding="utf-8")
            matches = emoji_pattern.findall(content)
            if matches:
                violations.append(f"{file_rel}: {set(matches)}")
        except UnicodeDecodeError:
            pass

    assert not violations, f"Emojis detected in tracked repository files: {violations}"
