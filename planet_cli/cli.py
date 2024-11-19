import click

@click.group()
@click.version_option(version="0.0.1", prog_name="planet-cli")
def main():
    """This CLI tool leverages the SentinelHub Catalog and Processing APIs"""
    pass



