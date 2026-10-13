# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Test that all repository Python source files contain valid SPDX headers and copyright notices."""

from pathlib import Path

REQUIRED_SPDX = "SPDX-License-Identifier: MIT"
REQUIRED_COPYRIGHT = "Copyright (c) 2026 ARPA Hellenic Logical Systems"

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PACKAGE_DIR = REPO_ROOT / "skillware_bench"


def test_package_source_spdx_headers():
    py_files = list(PACKAGE_DIR.rglob("*.py"))
    assert len(py_files) > 0, "No Python source files discovered in skillware_bench"

    for file_path in py_files:
        content = file_path.read_text(encoding="utf-8")
        lines = [line.strip() for line in content.splitlines()[:5]]

        has_spdx = any(REQUIRED_SPDX in line for line in lines)
        has_copyright = any(REQUIRED_COPYRIGHT in line for line in lines)

        assert has_spdx, f"Missing SPDX header in {file_path.relative_to(REPO_ROOT)}"
        assert has_copyright, f"Missing Copyright notice in {file_path.relative_to(REPO_ROOT)}"
