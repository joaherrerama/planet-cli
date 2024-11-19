""" Module provide a function that creates a config file post-installing the CLI """
import json
import os

def create_config_file() -> None:
    """
        Function create the config.json file
        after installing the CLI. If the file exists, the step is skipped
    """
    config_template = {
        "output-format": "tiff",
        "output-type": "visual"
    }

    config_file = "config.json"

    if not os.path.exists(config_file):
        with open(config_file, "w", encoding="utf-8") as config:
            json.dump(config_template, config, indent=4)
            print("Config file created, check planet-cli config --help for more information")
    else:
        print("Config file already exists...")

if __name__ == "__main__":
    create_config_file()
