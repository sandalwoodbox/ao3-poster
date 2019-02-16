import csv

import click
import jinja2

from . import ao3
from .exceptions import LoginRequired
from .exceptions import SessionExpired
from .exceptions import UnexpectedError
from .exceptions import ValidationError


@click.group()
def cli():
    pass


@cli.command()
@click.argument(
    'csv_file',
    type=click.File('r')
)
@click.option(
    '--work-text-template',
    type=click.File('r'),
    help=(
        "The path to a jinja2 template for generating work"
        "text from csv data"
    ),
)
def post(csv_file, work_text_template=None):
    """
    Post new works to ao3 from a csv spreadsheet
    """
    reader = csv.DictReader(csv_file)
    rows = list(reader)

    if work_text_template is not None:
        work_text_template = jinja2.Template(work_text_template.read())

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
                work_text_template=work_text_template,
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
                '{} uploaded successfully!\n{}'.format(work_title, work_url),
                fg='green',
            )

    ao3.logout(session)
