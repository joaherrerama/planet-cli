import os
from unittest.mock import patch
from click.testing import CliRunner
from cli_test_helpers import ArgvContext, shell
import pytest
from planet_cli import cli
from planet_cli.commands.search_commands import search

@pytest.fixture
def mock_process_api_manager():
    with patch('planet_cli.classes.process_api_manager.ProcessApiManager') as mocker_process_api:
        return mocker_process_api

@pytest.fixture
def mock_validate_time():
    with patch('planet_cli.commands.utils.validate_time') as mocker_validate_time:
        return mocker_validate_time

def test_search_group_help():
    """Test 'planet_cli config' displays help."""
    result = shell("planet-cli config --help")
    assert result.exit_code == 0

def test_invalid_dates(mock_process_api_manager, mock_validate_time):
    aoi_path = os.path.join(os.path.dirname(__file__), 'assets', 'aoi_test.geojson')
    result = shell(
        f'planet-cli search --aoi {aoi_path} --start-date 2020-01-20 --end-date 2019-01-20'
    )
    assert result.exit_code != 0
    assert result.stderr == "Usage: planet-cli search [OPTIONS]\nTry 'planet-cli search --help' for help.\n\nError: Invalid value: End time must be after start time.\n"

def test_search_fail():
    aoi_path = os.path.join(os.path.dirname(__file__), 'assets', 'aoi_test.geojson')
    result = shell(
        f'planet-cli search --aoi {aoi_path} --start-date 2020-01-20 --end-date 2020-02-20'
    )
    assert result.exit_code != 0

# def test_search(mock_process_api_manager, mock_validate_time):
#     runner = CliRunner()
#     mock_process = mock_process_api_manager.return_value
#     mock_process.process.return_value = "mock_data_request"
#     aoi_path = os.path.join(os.path.dirname(__file__), 'assets', 'aoi_test.geojson')
#     destinationi_path = os.path.join(os.path.dirname(__file__), 'assets')
#     result = runner.invoke(
#         search, [
#             '--aoi', aoi_path, 
#             '--start-date', '2019-01-20 08:00', 
#             '--end-date', '2020-11-20 18:00', 
#             '--destination-folder', destinationi_path, 
#             '--client-id', 'mock-client-id',
#             '--client-secret', 'mock-client-secret',
#             '--output-type', 'visual', 
#             '--output-format', 'tiff'
#         ]
#     )
#     import pdb;pdb.set_trace()
#     assert result.exit_code == 0
#     assert "Processing time image" in result.output
#     mock_process.process.assert_called_once_with(
#         aoi_path, 
#         '2019-01-20 08:00', 
#         '2020-11-20 18:00', 
#         'mock-client-id', 
#         'mock-client-secret', 
#         'visual', 
#         'tiff'
#     )
#     mock_process.download.assert_called_once_with("mock_data_request", '/mock/folder')
#     assert "The Image has been successfully stored in /mock/folder." in result.output

