# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Unit tests for the Skillware-Bench CLI."""

from unittest.mock import MagicMock
from rich.console import Console
from skillware_bench.cli import cmd_list, cmd_run, cmd_compare


def test_cli_list():
    console = Console(record=True)
    args = MagicMock()
    cmd_list(args, console)
    output = console.export_text()
    assert "Crucible Catalog" in output
    assert "gmail" in output
    assert "companies_house" in output
    assert "wallet_screening" in output


def test_cli_run():
    console = Console(record=True, width=120)
    args = MagicMock()
    args.suite = None
    args.model = "test-model"
    args.mock = True
    args.live = False
    args.adapter = None
    args.export = False
    cmd_run(args, console)
    output = console.export_text()
    assert "Skillware-Bench Empirical Progression" in output
    assert "office_gmail_01" in output


def test_cli_compare():
    console = Console(record=True, width=120)
    args = MagicMock()
    args.suite = "gmail"
    args.model = "test-model"
    cmd_compare(args, console)
    output = console.export_text()
    assert "Crucible Deep Dive" in output
    assert "Generic Baseline (Without Skillware)" in output
    assert "Skillware Equipped" in output
    assert "Empirical Lift" in output


def test_cli_check_env():
    from skillware_bench.cli import cmd_check_env

    console = Console(record=True, width=120)
    args = MagicMock()
    cmd_check_env(args, console)
    output = console.export_text()
    assert "Verification" in output
    assert "OPENAI_API_KEY" in output
    assert "COMPANIES_HOUSE" in output


def test_cli_run_with_custom_adapter(tmp_path):
    adapter_code = """
from skillware_bench.core.adapters.base import BaseModelAdapter, ModelResponse

class CustomTestAdapter(BaseModelAdapter):
    def chat(self, messages, tools=None, system_prompt=None, **kwargs):
        return ModelResponse(content="Custom BYOM response")
"""
    adapter_file = tmp_path / "custom_test_adapter.py"
    adapter_file.write_text(adapter_code, encoding="utf-8")

    console = Console(record=True, width=120)
    args = MagicMock()
    args.suite = "gmail"
    args.model = "custom-test"
    args.mock = False
    args.live = True
    args.adapter = str(adapter_file)
    args.export = False

    cmd_run(args, console)
    output = console.export_text()
    assert "LIVE (real API execution)" in output
    assert "office_gmail_01" in output
