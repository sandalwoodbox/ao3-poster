import click
import csv
from google.auth.exceptions import DefaultCredentialsError

from . import ao3
from .exceptions import LoginRequired
from .exceptions import SessionExpired
from .exceptions import ValidationError
from .utils.google_sheets import get_sheet_data


@click.group()
def cli():
    pass


@cli.command()
@click.argument('sheet_id')
@click.argument('outfile', type=click.File('wb'))
@click.option(
    '--count',
    default=1,
    type=click.IntRange(1, 10),
    help='How many rows [1-10] to import from the sheet',
)
def get_sheet(sheet_id, outfile, count):
    click.echo('\nDownloading google sheet data...')
    try:
        headers, rows = get_sheet_data(sheet_id, count)
    except DefaultCredentialsError as exc:
        raise click.ClickException(str(exc))

    click.secho('Done', fg='green')

    writer = csv.DictWriter(outfile, fieldnames=headers)

    for row in rows[:count]:
        writer.writerow(row)


@cli.command()
@click.argument(
    'csv',
    type=click.File('rb')
)
def post(csv):
    username = click.prompt('Username or email')
    password = click.prompt(
        'Password',
        hide_input=True,
        confirmation_prompt=True,
    )
    session = ao3.login(username, password)
    if session is None:
        raise click.ClickException('Login failed. Please try again.')
    else:
        click.secho('Login successful.', fg='green')

    reader = csv.DictReader(csv)
    for row in reader:
        work_title = row.get('Work Title', 'Unknown Work')
        click.echo('Uploading to AO3: {}'.format(work_title))

        try:
            work_url = ao3.post(session, row)
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

    ao3.logout(session)
