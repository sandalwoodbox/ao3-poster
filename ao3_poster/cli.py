import click
import csv
import jinja2
from google.auth.exceptions import DefaultCredentialsError

from . import ao3
from .exceptions import LoginRequired
from .exceptions import SessionExpired
from .exceptions import UnexpectedError
from .exceptions import ValidationError
from .utils.google_sheets import get_sheet_data


@click.group()
def cli():
    pass


@cli.command()
@click.argument('sheet_id')
@click.argument('outfile', type=click.File('w'))
@click.option(
    '--count',
    default=1,
    type=click.IntRange(1, 10),
    help='How many rows [1-10] to import from the sheet',
)
def get_sheet(sheet_id, outfile, count):
    """
    Download a google sheet as a csv.
    """
    click.echo('\nDownloading google sheet data...')
    try:
        headers, rows = get_sheet_data(sheet_id, count)
    except DefaultCredentialsError as exc:
        raise click.ClickException(str(exc))

    click.secho('Done', fg='green')

    writer = csv.DictWriter(outfile, fieldnames=headers)
    writer.writeheader()
    for row in rows[:count]:
        writer.writerow(row)


@cli.command()
@click.argument(
    'csv_file',
    type=click.File('r')
)
@click.option(
    '--body-template',
    type=click.File('r'),
)
def post(csv_file, body_template=None):
    """
    Post a csv of data to ao3.
    """
    reader = csv.DictReader(csv_file)
    rows = list(reader)

    if body_template is not None:
        body_template = jinja2.Template(body_template.read())

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

    for row in rows:
        work_title = row.get('Work Title', 'Unknown Work')
        click.echo('Uploading to AO3: {}'.format(work_title))

        try:
            work_url = ao3.post(
                session=session,
                data=row,
                body_template=body_template,
            )
        except ValidationError as exc:
            click.echo('Validation errors encountered while processing {}:\n{}'.format(
                work_title,
                '\n'.join(exc.errors)
            ))
            click.secho(
                '{} was not uploaded'.format(work_title),
                fg='red',
            )
        except UnexpectedError:
            click.secho('Server error encountered while processing {}'.format(work_title))
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
