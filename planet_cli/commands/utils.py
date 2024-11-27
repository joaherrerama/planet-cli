import click
from dateutil.parser import parse


def validate_time(ctx, param, value):
    try:
        return parse(value)
    except Exception:
        raise click.BadParameter(
            f"Invalid time format: {value}. Use a format like 'YYYY-MM-DD HH:MM'."
        )
