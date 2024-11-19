import json

from planet_cli.classes.error_manager import CredentialNotFoundError 


class ConfigManager:

    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.__credendial_key = "credential-key"
        self.__output_type_key = "output-type"
        self.__output_format_key = "output-format"
        self.__valid_types = ["Visual", "NDVI"]
        self.__valid_formats = ["TIFF", "PNG"]


    def __credential_validation(self,credential) -> bool:
        """
            This function validates that the credential provided 
            is valid.
        """
        return True
    

    def __output_type_validator(self,output_type) -> bool:
        return True if output_type in self.__valid_types else False


    def __output_format_validator(self,output_format) -> bool:
        return True if output_format in self.__valid_formats else False


    def __get_config(self) ->  json:
        """
            Function returns the config.json file
            or an empty dict in case the file does not exist.
        """
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def set_credentials(self, credential: str) -> None:
        """
        Save the Sentinel Hub credentials for API authorization
            - credentials: str -> Token from Sentinel Hub
        """

        if self.__credential_validation(credential):
            config_json = self.__get_config()
            config_json[self.__credendial_key] = credential

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config_json, f)


    def set_output_type(self, output_type: str) -> None: 
        """Save output type"""
        if self.__output_type_validator(output_type):
            config_json = self.__get_config()
            config_json[self.__output_type_key] = output_type

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config_json, f)


    def set_outout_format(self, output_format: str) -> None:
        """Save credentials for future excecutions"""
        if self.__output_format_validator(output_format):
            config_json = self.__get_config()
            config_json[self.__output_format_key] = output_format

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config_json, f)


    def get_credentials(self) -> str:
        """ Return the credentials saved"""
        config_json = self.__get_config()
        if self.__credendial_key in config_json.keys():
            return config_json[self.__credendial_key]

        raise CredentialNotFoundError(
            "Credentials is not defined, please use --credential or \
                planet-cli config credential SENTINEL_HUB_CREDENTIAL."
        )


    def get_output_type(self) -> str:
        """ Return the credentials saved"""
        config_json = self.__get_config()
        if self.__output_type_key in config_json.keys():
            return config_json[self.__output_type_key]

        return "Visual"


    def get_output_format(self) -> str:
        """ Return the credentials saved"""
        config_json = self.__get_config()
        if self.__output_format_key in config_json.keys():
            return config_json[self.__output_format_key]

        return "TIFF"
