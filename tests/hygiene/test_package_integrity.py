# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Test packaging integrity, version consistency, and module exports."""

from pathlib import Path
import tomllib
import skillware_bench

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_version_consistency():
    pyproject_path = REPO_ROOT / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    project_version = data["project"]["version"]
    assert (
        skillware_bench.__version__ == project_version
    ), f"Version mismatch: __init__.py ({skillware_bench.__version__}) vs pyproject.toml ({project_version})"


def test_package_exports():
    assert hasattr(skillware_bench, "__version__")
    assert hasattr(skillware_bench, "__author__")
    assert "ARPA Hellenic Logical Systems" in skillware_bench.__author__
