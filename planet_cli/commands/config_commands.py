""" This module handles the commands for config subcommand"""
import click
from planet_cli.classes.config_manager import ConfigManager


@click.group()
def config():
    """This section allows you to set your credentials, output-format and output-type"""
    click.echo("This section allows you to set your credentials, output-format and output-type")


@config.command("credentials")
@click.argument("client-id")
@click.argument("client-secret")
def credentials(client_id:str, client_secret: str):
    """
    This command receives client id and client secret
    providing by Sentinel Hub and store it for future usage
        - CLIENT-ID: parameter found in settings OAuth clients section
        - CLIENT-SECRET: parameter found in settings OAuth clients section
    """
    config = ConfigManager()
    config.set_credentials(client_id, client_secret)
    click.echo("Credentials have been successfully stored")


@config.command("output-format")
@click.argument("output_format", type=click.Choice(["tiff", "png"]), nargs=1)
def output_format(output_format):
    """output-format (default: tiff) - Set output format selection for general purpose."""
    config = ConfigManager()
    config.set_output_format(output_format)
    click.echo(f"The output format '{output_format}' is successfully stored'.")


@config.command("output-type")
@click.argument("output_type", type=click.Choice(["visual", "ndvi"]), nargs=1)
def output_format(output_format):
    """output-type (default: visual) - Set output type selection for general purpose."""
    config = ConfigManager()
    config.set_output_format(output_format)
    click.echo(f"The output type '{output_format}' is successfully stored'.")


