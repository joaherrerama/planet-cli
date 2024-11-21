""" This module handles the commands for the search subcommands"""

import os
import click
from planet_cli.classes.geometry_handler import GeometryHandler
from planet_cli.classes.proccess_api_manager import ProcessApiManager
from planet_cli.commands.utils import validate_time



@click.command("search")
@click.option(
    "--aoi", 
    type=click.Path(exists=True),
    required=True,
    help="Area of interest in GeoJSON format"
)
@click.option(
    "--start-date",
    required=True,
    callback=validate_time,
    help="Start time of the range (e.g., '2019-01-20 08:00')."
)
@click.option(
    "--end-date",
    required=True, 
    callback=validate_time, 
    help="End time of the range (e.g., '2020-11-20 18:00')."
)
@click.option(
    '--destination-folder',
    default=os.getcwd(), 
    help='The destination folder where the elements should be saved'
)
@click.option(
    "--client-id", 
    type=str,
    help="Client-id from SentinelHub. if not it will use the one defined in config (planet-config config)"
)
@click.option(
    "--client-secret", 
    type=str,
    help="Client-secret from SentinelHub. if not it will use the one defined in config (planet-config config)"
)
@click.option(
    "--output-type", 
    type=click.Choice(['visual', 'ndvi'], case_sensitive=False),
    help="Format of the file Visual or NDVI, if not defined it uses Visual or the one defined in config"
)
@click.option(
    "--output-format", 
    type=click.Choice(['tiff', 'png'],case_sensitive=False),
    help="Format of the file Tiff or PNG, if not defined it uses Tiff or the one defined in config"
)
def search(aoi: str, start_date:str, end_date:str, destination_folder:str, client_id: str, client_secret: str, output_type: str, output_format: str):
    """search and download the most cloudless image with the params given."""

    if end_date <= start_date:
        raise click.BadParameter("End time must be after start time.")

    click.echo(f"Processing time image from {start_date} to {end_date}.")

    process_class = ProcessApiManager()

    data_request = process_class.process(aoi, start_date, end_date, client_id, client_secret, output_type, output_format)
    process_class.download(data_request, destination_folder)

    click.echo(f"The Image has been successfully stored in {destination_folder}.")
