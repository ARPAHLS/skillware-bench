# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Test packaging integrity, version consistency, and module exports."""

from pathlib import Path
import re
import sys
import skillware_bench

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_version_consistency():
    pyproject_path = REPO_ROOT / "pyproject.toml"
    if tomllib is not None:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
        project_version = data["project"]["version"]
    else:
        content = pyproject_path.read_text(encoding="utf-8")
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        assert match, "Could not extract version from pyproject.toml"
        project_version = match.group(1)

    assert (
        skillware_bench.__version__ == project_version
    ), f"Version mismatch: __init__.py ({skillware_bench.__version__}) vs pyproject.toml ({project_version})"


def test_package_exports():
    assert hasattr(skillware_bench, "__version__")
    assert hasattr(skillware_bench, "__author__")
    assert "ARPA Hellenic Logical Systems" in skillware_bench.__author__
