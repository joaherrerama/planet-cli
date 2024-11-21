"""
    This module contains the class AuthorizationManager
    to handle the API authorization.
"""
from datetime import datetime
from planet_cli.classes.config_manager import ConfigManager
from planet_cli.classes.utils import request_token

class AuthorizationManager:
    """
    This class handles API authorization using client_id and client_secret
    to retrieve an access token.
    """

    def __init__(self):
        """
        Initialize the AuthorizationManager with the authorization URL.
        """
        self.auth_url = 'https://services.sentinel-hub.com/auth/realms/main/protocol/openid-connect/token'

    def __token_validator(self, token_object):
        current_time = datetime.now()
        expires_at = datetime.fromtimestamp(token_object["expires_at"])

        return True if current_time < expires_at else False
    
    def get_token(self, client_id: str, client_secret: str) -> str:
        """
        Retrieve an access token using the provided client_id and client_secret.
        """

        # Validate Token in Config
        token_object = ConfigManager.get_token()
        if self.__token_validator(token_object):
            return token_object["access_token"]
        else:
            token = request_token(client_id, client_secret)
            ConfigManager().set_token(token)
            return token["access_token"]