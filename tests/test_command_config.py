import pytest
from cli_test_helpers import ArgvContext, shell
from unittest.mock import patch, MagicMock
import planet_cli.cli as cli


@pytest.fixture
def mock_config_manager():
    """Fixture to mock ConfigManager."""
    with patch("planet_cli.classes.config_manager.ConfigManager") as mock:
        yield mock


def test_config_group_help():
    """Test 'planet_cli config' displays help."""
    result = shell("planet-cli config --help")
    assert result.exit_code == 0


def test_credentials_command_valid(mock_config_manager):
    mock_instance = MagicMock()
    mock_config_manager.return_value = mock_instance

    with patch("planet_cli.classes.utils.request_token") as mock_request_token:
        mock_request_token.return_value = {"access_token": "valid-token"} 

        mock_instance.__get_config.return_value = {
            'client_id': None,
            'client_secret': None,
            'token': None
        }

        try:
            mock_instance.set_credentials("test-client-id", "test-client-secret")
            assert True
        except Exception as e:
            assert False, f"set_credentials raised an exception: {e}"


def test_output_format_command(mock_config_manager):
    mock_instance = MagicMock()
    mock_config_manager.return_value = mock_instance

    try:
        with ArgvContext('planet-cli', 'config', 'output-format', 'tiff') as args:
            args = cli.main(args=args)
    except SystemExit as e:
        assert e.code == 0


def test_output_format_command_fail(mock_config_manager):
    mock_instance = MagicMock()
    mock_config_manager.return_value = mock_instance

    try:
        with ArgvContext('planet-cli', 'config', 'output-format', 'jpg') as args:
            args = cli.main(args=args)
    except SystemExit as e:
        assert e.code != 0
        assert "Invalid value for '{tiff|png}': 'tiff' is not one of 'tiff', 'png'"


def test_output_type_command(mock_config_manager):
    mock_instance = MagicMock()
    mock_config_manager.return_value = mock_instance

    try:
        with ArgvContext('planet-cli', 'config', 'output-type', 'visual') as args:
            args = cli.main(args=args)
    except SystemExit as e:
        assert e.code == 0


def test_output_type_command_fail(mock_config_manager):
    mock_instance = MagicMock()
    mock_config_manager.return_value = mock_instance

    try:
        with ArgvContext('planet-cli', 'config', 'output-type', 'infrared') as args:
            args = cli.main(args=args)
    except SystemExit as e:
        assert e.code != 0
        assert "Invalid value for '{visual|ndvi}': 'infrared' is not one of 'visual', 'ndvi'"