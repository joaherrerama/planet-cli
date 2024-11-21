"""
    Top Level Module - Here most of the general commands are defined
    CLI counts with:
        planet-cli
            - config
                - credentials
                    -ARGS
                    --client-id
                    --secret-id 
                - output-format
                    --of
                - output-type
                    --ot
            
            - search 
                OPTIONS
                    --aoi (mandatory)
                    --toi (mandatory)
                    --output-format (Default: TIFF)
                    --output-type (Default: Visual)
                    --credentials (mandatory if not defined)
"""

import click
from planet_cli.commands.config_commands import config
from planet_cli.commands.search_commands import search

@click.group()
@click.version_option(version="0.0.1", prog_name="planet-cli")
def main():
    """This CLI tool leverages the SentinelHub Catalog and Processing APIs"""
    click.echo("This CLI tool leverages the SentinelHub Catalog and Processing APIs")

main.add_command(config)
main.add_command(search)
