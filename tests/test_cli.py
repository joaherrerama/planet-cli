"""
Tests for command line interface (CLI).
"""
from importlib import import_module
from importlib.metadata import version
from os import linesep
from unittest.mock import patch

import pytest
from cli_test_helpers import ArgvContext, shell

import planet_cli.cli


def test_main_module():
    """
    Exercise (most of) the code in the ``__main__`` module.
    """
    import_module("planet_cli.__main__")


def test_runas_module():
    """
    Can this package be run as a Python module?
    """
    result = shell("python -m planet-cli --help")
    assert result.exit_code == 0


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    result = shell("planet-cli --help")
    assert result.exit_code == 0


@patch("planet_cli.cli.dispatch")
def test_usage(mock_dispatch):
    """
    Does CLI abort w/o arguments, displaying usage instructions?
    """
    with ArgvContext("planet-cli"), pytest.raises(SystemExit):
        planet_cli.cli.main()

    assert not mock_dispatch.called, "CLI should stop execution"

    result = shell("planet-cli")

    assert "usage:" in result.stderr


def test_version():
    """
    Does --version display information as expected?
    """
    expected_version = version("planet-cli")
    result = shell("planet-cli --version")

    assert result.stdout == f"{expected_version}{linesep}"
    assert result.exit_code == 0