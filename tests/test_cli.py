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
    console = Console(record=True)
    args = MagicMock()
    args.suite = None
    args.model = "test-model"
    args.mock = True
    args.export = False
    cmd_run(args, console)
    output = console.export_text()
    assert "Skillware-Bench Empirical Progression" in output
    assert "office_gmail_01" in output


def test_cli_compare():
    console = Console(record=True)
    args = MagicMock()
    args.suite = "gmail"
    args.model = "test-model"
    cmd_compare(args, console)
    output = console.export_text()
    assert "Crucible Deep Dive" in output
    assert "Generic Baseline (Without Skillware)" in output
    assert "Skillware Equipped" in output
    assert "Empirical Lift" in output
