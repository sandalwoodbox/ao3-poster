from google.auth.exceptions import DefaultCredentialsError
import click

from .utils.google_sheets import get_sheet_data


@click.command()
@click.argument('sheet_id')
def cli(sheet_id):
    try:
        headers, rows = get_sheet_data(sheet_id)
    except DefaultCredentialsError as exc:
        raise click.ClickException(str(exc))

    import pdb; pdb.set_trace()
