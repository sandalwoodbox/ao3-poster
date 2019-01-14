import click
from google.auth.exceptions import DefaultCredentialsError

from . import ao3
from .session import load_session_cookies
from .session import save_session_cookies
from .exceptions import LoginRequired
from .exceptions import SessionExpired
from .exceptions import ValidationError
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
    session_cookies = ao3.login(username, password)
    if session_cookies is None:
        click.secho('Login failed. Please try again.', fg='red')
    else:
        save_session_cookies(session_cookies)
        click.secho('Login successful. Session id saved.')


@cli.command()
def logout():
    """
    End your ao3 session
    """
    session_cookies = load_session_cookies()
    if session_cookies is not None:
        ao3.logout(session_cookies)
        save_session_cookies(None)


@cli.command()
@click.argument('sheet_id')
@click.option(
    '--count',
    default=1,
    type=click.IntRange(1, 10),
    help='How many rows [1-10] to import from the sheet',
)
def post(sheet_id, count):
    try:
        headers, rows = get_sheet_data(sheet_id, count)
    except DefaultCredentialsError as exc:
        raise click.ClickException(str(exc))

    for row in rows[:count]:
        work_title = row.get('Work Title', 'Unknown Work')
        click.echo('Uploading to AO3: {}'.format(work_title))

        session_cookies = load_session_cookies()

        try:
            work_url = ao3.post(session_cookies, row)
        except ValidationError as exc:
            click.echo('Validation errors encountered while processing {}: {}'.format(
                work_title,
                ', '.join(exc.errors)
            ))
            click.secho(
                '{} was not uploaded'.format(work_title),
                fg='red',
            )
        except LoginRequired:
            raise click.ClickException('Login is required. Please log in with `ao3 login`')
        except SessionExpired:
            raise click.ClickException('Login session expired. Please log in again with `ao3 login`')
        else:
            click.secho(
                '{} uploaded successfully! {}'.format(work_title, work_url),
                fg='green',
            )
