from google.auth.exceptions import DefaultCredentialsError
import click

from . import ao3
from .config import save_session_id
from .config import load_session_id
from .utils.google_sheets import get_sheet_data


@click.group()
def cli():
    pass


@cli.command()
def login():
    """
    Start a new ao3 session
    """
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
        save_session_id(session_id)
        click.secho('Login successful. Session id saved.')


@cli.command()
def logout():
    """
    End your ao3 session
    """
    session_id = load_session_id()
    if session_id is not None:
        ao3.logout(session_id)
        save_session_id(None)


@cli.command()
@click.argument('sheet_id')
def post(sheet_id):
    try:
        headers, rows = get_sheet_data(sheet_id)
    except DefaultCredentialsError as exc:
        raise click.ClickException(str(exc))

    import pdb; pdb.set_trace()


