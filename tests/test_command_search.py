import os
from unittest.mock import patch
from cli_test_helpers import shell
import pytest


@pytest.fixture
def mock_process_api_manager():
    with patch(
        "planet_cli.classes.process_api_manager.ProcessApiManager"
    ) as mocker_process_api:
        return mocker_process_api


@pytest.fixture
def mock_validate_time():
    with patch("planet_cli.commands.utils.validate_time") as mocker_validate_time:
        return mocker_validate_time


def test_search_group_help():
    """Test 'planet_cli config' displays help."""
    result = shell("planet-cli config --help")
    assert result.exit_code == 0


def test_invalid_dates(mock_process_api_manager, mock_validate_time):
    aoi_path = os.path.join(os.path.dirname(__file__), "assets", "aoi_test.geojson")
    result = shell(
        f"planet-cli search --aoi {aoi_path} --start-date 2020-01-20 --end-date 2019-01-20"
    )
    assert result.exit_code != 0
    error = "Usage: planet-cli search [OPTIONS]\nTry 'planet-cli search --help' for help.\n\nError: Invalid value: End time must be after start time.\n"
    assert result.stderr == error


def test_search_fail():
    aoi_path = os.path.join(os.path.dirname(__file__), "assets", "aoi_test.geojson")
    result = shell(
        f"planet-cli search --aoi {aoi_path} --start-date 2020-13-20 --end-date 2020-02-20"
    )
    assert result.exit_code != 0


# If credentials are setup then it would work else it fails
def test_search():
    aoi_path = os.path.join(os.path.dirname(__file__), "assets", "aoi_test.geojson")
    result = shell(
        f"planet-cli search --aoi {aoi_path} --start-date 2020-01-20 --end-date 2020-02-20"
    )
    assert result.exit_code == 0
    output = "This CLI tool leverages the SentinelHub Catalog and Processing APIs\n \
    Processing time image from 2020-01-20 00:00:00 to 2020-02-20 00:00:00.\n\
    The Image has been successfully stored in /home/jorge/repositories/planet-cli.\n"
    assert result.stdout == output
