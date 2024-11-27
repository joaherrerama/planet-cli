"""
Tests for command line interface (CLI).
"""

from importlib import import_module
from importlib.metadata import version
from os import linesep
from cli_test_helpers import shell


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
    assert result.exit_code == 1


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    result = shell("planet-cli --help")
    assert result.exit_code == 0


def test_version():
    """
    Does --version display information as expected?
    """
    expected_version = version("planet-cli")
    result = shell("planet-cli --version")

    assert result.stdout == f"planet-cli, version {expected_version}{linesep}"
    assert result.exit_code == 0
