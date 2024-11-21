"""
    This module contains the class ConfigManager to handle all methods regarding the confing file
"""
from datetime import datetime
import json
import os

from planet_cli.classes.error_manager import CredentialNotFoundError
from planet_cli.classes.utils import request_token 


class ConfigManager:
    """
        This class manage all the operations and attributes
        to feed the configuration settings
    """

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.config_file = os.path.join(base_dir, ".config", "config.json")
        self._client_id_key = "client-id"
        self._client_secret_key = "client-secret"
        self._token_key = "token"
        self._output_type_key = "output-type"
        self._output_format_key = "output-format"


    def __get_config(self) ->  json:
        """
            Function returns the config.json file
            or an empty dict in case the file does not exist.
        """

        #try:
        with open(self.config_file, "r", encoding="utf-8") as f:
            return json.load(f)
        #except FileNotFoundError:
        #    return {}
        
    def set_token(self, token:dict) -> None:
        """ Save token in case needs to be refresh"""
        config_json = self.__get_config()
        config_json[self._token_key] = {
            "token":token,
            "createdAt": datetime.now()
        }

    def set_credentials(self, client_id: str, client_secret: str) -> None:
        """
        Save the Sentinel Hub credentials for API authorization
            - credentials: str -> Token from Sentinel Hub
        """
        token = request_token(client_id, client_secret)

        if token:
            config_json = self.__get_config()
            config_json[self._client_id_key] = client_id
            config_json[self._client_secret_key] = client_secret
            config_json[self._token_key] = token

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config_json, f)


    def set_output_type(self, output_type: str) -> None: 
        """Save output type"""
        if self.__output_type_validator(output_type):
            config_json = self.__get_config()
            config_json[self._output_type_key] = output_type

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config_json, f)


    def set_output_format(self, output_format: str) -> None:
        """Save credentials for future executions"""
        if self.__output_format_validator(output_format):
            config_json = self.__get_config()
            config_json[self._output_format_key] = output_format

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config_json, f)


    def get_credentials(self) -> tuple[str, str]:
        """ 
            Return the saved credentials

            In case the credentials does not exist it will return 
            CredentialNotFoundError with a handful message

            Returns:
                tuple[str, str] -> it contains Client_id and Client_secret
        """
        config_json = self.__get_config()

        try:
            return config_json[self._client_id_key], config_json[self._client_secret_key]
        except NameError as e:
            raise CredentialNotFoundError(
                "Credentials is not defined, please use --client-id and --client-secret options  or \
                    planet-cli config credentials CLIENT_ID CLIENT_SECRET."
            )


    def get_output_type(self) -> str:
        """ Return the credentials saved"""
        config_json = self.__get_config()
        if self._output_type_key in config_json.keys():
            return config_json[self._output_type_key]


    def get_output_format(self) -> str:
        """ Return the credentials saved"""
        config_json = self.__get_config()
        if self._output_format_key in config_json.keys():
            return config_json[self._output_format_key]
    
    def get_token(self) -> str:
        config_json = self.__get_config()
        
        if self._token_key in config_json.keys():
            return config_json[self._token_key]
        else:
            return None