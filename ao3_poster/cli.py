import json
import os

from google.auth.exceptions import DefaultCredentialsError
import click

from . import ao3
from .constants import AO3_DIRECTORY
from .utils.google_sheets import get_sheet_data


CONFIG_FILE = os.path.join(AO3_DIRECTORY, 'config.json')


@click.group()
def cli():
    pass


@cli.command()
def login():
    username = click.prompt('Username or email')
    password = click.prompt(
        'Password',
        hide_input=True,
        confirmation_prompt=True,
    )
    session_id = ao3.login(username, password)
    if session_id is None:
        click.secho('Login failed. Please try again.', fg='red')
    else:
        if not os.path.exists(AO3_DIRECTORY):
            os.makedirs(AO3_DIRECTORY)

        with open(CONFIG_FILE, 'w') as fp:
            json.dump({'session_id': session_id}, fp)

        click.secho('Login successful. Session id saved.')


@cli.command()
@click.argument('sheet_id')
def post(sheet_id):
    try:
        headers, rows = get_sheet_data(sheet_id)
    except DefaultCredentialsError as exc:
        raise click.ClickException(str(exc))

    import pdb; pdb.set_trace()


