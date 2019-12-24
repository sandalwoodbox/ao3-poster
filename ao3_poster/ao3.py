# encoding: utf-8

import os
import re

import bs4
import requests

from .exceptions import LoginRequired
from .exceptions import SessionExpired
from .exceptions import UnexpectedError
from .exceptions import ValidationError


AO3_URL = os.environ.get('AO3_URL', 'https://archiveofourown.org/')

if not AO3_URL.endswith('/'):
    AO3_URL += '/'


REQUEST_HEADERS = {
    # AO3 blocks python-requests by default so we need to fake a different user agent.
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',  # noqa: E501
}

LOGIN_URL = '{}users/login'.format(AO3_URL)
LOGOUT_URL = '{}users/logout'.format(AO3_URL)
# URL for new works form
POST_FORM_URL = '{}works/new'.format(AO3_URL)
# URL to post to for creating new works
POST_ACTION_URL = '{}works'.format(AO3_URL)

# URL you are redirected to if session expires
AUTH_ERROR_URL = '{}auth_error'.format(AO3_URL)
# URL you are redirected to if cookie is "lost"
LOST_COOKIE_URL = '{}lost_cookie'.format(AO3_URL)

USER_DASHBOARD_REGEX = re.compile(r'^/users/([^/]+)$')

HEADER_MAP = {
    'Rating': 'work[rating_string]',
    'Archive Warnings': 'work[archive_warning_strings][]',
    'Fandoms': 'work[fandom_string]',
    'Category': 'work[category_string][]',
    'Relationships': 'work[relationship_string]',
    'Characters': 'work[character_string]',
    'Additional Tags': 'work[freeform_string]',
    'Work Title': 'work[title]',
    'Creator/Pseud(s)': 'work[author_attributes][ids][]',
    'Add co-creators?': 'pseud[byline]',
    'Summary': 'work[summary]',
    'Notes at the beginning': 'work[notes]',
    'Notes at the end': 'work[endnotes]',
    'Parent Work URL': 'work[parent_attributes][url]',
    'Parent Work Title': 'work[parent_attributes][title]',
    'Parent Work Author': 'work[parent_attributes][author]',
    'Language': 'work[language_id]',
    'Work text': 'work[chapter_attributes][content]',
}


def _validate_response_url(response):
    if response.status_code == 302:
        url = response.headers['Location']
    else:
        url = response.url

    if url == LOGIN_URL:
        raise LoginRequired

    expired_session_urls = (
        AUTH_ERROR_URL,
        LOST_COOKIE_URL,
    )
    if url in expired_session_urls:
        raise SessionExpired


def get_authenticity_token(text, form_id):
    strainer = bs4.SoupStrainer(id=form_id)
    soup = bs4.BeautifulSoup(text, 'lxml', parse_only=strainer)
    return soup.find(attrs={'name': 'authenticity_token'})['value']


def get_languages(text):
    strainer = bs4.SoupStrainer(id='work_language_id')
    soup = bs4.BeautifulSoup(text, 'lxml', parse_only=strainer)
    options = soup.find_all('option')
    return {
        option.string: option['value']
        for option in options
        if option['value']
    }


def get_pseuds(text):
    strainer = bs4.SoupStrainer(id='work_author_attributes_ids')
    soup = bs4.BeautifulSoup(text, 'lxml', parse_only=strainer)
    options = soup.find_all('option')
    if options:
        return {
            option.string: option['value']
            for option in options
        }

    # If there are no options, this is the single case, which uses a single input field.
    # soup.children returns a new iterator on each access.
    user_id = soup.find(id='work_author_attributes_ids')['value']

    strainer = bs4.SoupStrainer('a', href=USER_DASHBOARD_REGEX)
    soup = bs4.BeautifulSoup(text, 'lxml', parse_only=strainer)

    dashboard_href = soup.a['href']
    matches = USER_DASHBOARD_REGEX.search(dashboard_href)
    pseud = matches.group(1)

    return {
        pseud: user_id,
    }


def get_validation_errors(text):
    errors = []

    soup = bs4.BeautifulSoup(text, 'lxml')
    error = soup.find(id='error')
    if error:
        errors += [li.text for li in error.find_all('li')]

    new_work_form = soup.find('form', id='new_work')
    if new_work_form:
        invalid_pseuds = new_work_form.find('h4', text=re.compile(r'These pseuds are invalid:'))
        if invalid_pseuds:
            errors += ['Invalid pseuds listed as authors']

    return errors


def build_post_data(data, pseuds, languages, work_text_template=None):
    post_data = []
    errors = []

    for key, value in data.items():
        post_key = HEADER_MAP.get(key)

        if post_key is None:
            continue

        if key == 'Creator/Pseud(s)':
            values = value.split(',')
            invalid_pseuds = set(values) - set(pseuds)

            if invalid_pseuds:
                errors.append((
                    'The following are not your pseuds: {}.'
                    ' Please use "Add co-creators?" for non-pseud co-creators.'
                ).format(
                    ', '.join(sorted(invalid_pseuds))
                ))
            else:
                value = ','.join([pseuds[v] for v in values])

        if key == 'Language':
            if value not in languages:
                errors.append('Unknown language: {}'.format(value))
            else:
                value = languages[value]

        if '[]' in post_key:
            for item in value.split(','):
                post_data.append((
                    post_key,
                    item.strip(),
                ))
        else:
            post_data.append((
                post_key,
                value.strip(),
            ))

    if errors:
        raise ValidationError(errors)

    if work_text_template is not None and 'Work text' not in data:
        post_key = HEADER_MAP['Work text']
        value = work_text_template.render(data=data)
        post_data.append((
            post_key,
            value,
        ))

    return post_data


def post(session, data, work_text_template=None):
    # Takes data, posts to ao3, and returns the URL for the created work
    # or raises an exception with validation errors.

    # First, get an authenticity token.
    response = session.get(
        POST_FORM_URL,
        allow_redirects=False,
    )
    _validate_response_url(response)
    authenticity_token = get_authenticity_token(response.text, 'work-form')
    languages = get_languages(response.text)
    pseuds = get_pseuds(response.text)

    # Now get a pseud->id mapping

    # Now post data.
    post_data = build_post_data(
        data=data,
        languages=languages,
        pseuds=pseuds,
        work_text_template=work_text_template,
    )
    post_data += [
        ('utf8', '✓'),
        ('authenticity_token', authenticity_token),

        # Trigger a preview
        ('preview_button', 'Preview'),

        # Without this attribute, AO3 will try to set the translation column to NULL
        # if the work is a remix of another work.
        ('work[parent_attributes][translation]', '0'),
    ]
    response = session.post(
        POST_ACTION_URL,
        post_data,
        allow_redirects=False,
    )

    if response.status_code == 500:
        raise UnexpectedError('Received server error')

    _validate_response_url(response)

    if response.url == POST_ACTION_URL:
        validation_errors = get_validation_errors(response.content)
        if validation_errors:
            raise ValidationError(validation_errors)

    if response.status_code == 302:
        return response.headers['Location']

    return response.url


def _is_failed_login(response):
    return "The password or user name you entered doesn't match our records." in response.text


def login(username, password):
    # returns a logged-in ao3 session id or None if login failed.
    session = requests.Session()
    session.headers.update(REQUEST_HEADERS)

    # First, get an authenticity token.
    response = session.get(LOGIN_URL)
    authenticity_token = get_authenticity_token(response.text, 'loginform')

    # Now log in.
    login_data = {
        'utf8': '✓',
        'authenticity_token': authenticity_token,
        'user[login]': username,
        'user[password]': password,
        'commit': 'Log In',
    }

    response = session.post(
        LOGIN_URL,
        login_data,
        allow_redirects=False,
    )

    if _is_failed_login(response):
        return None

    return session


def logout(session):
    session.get(LOGOUT_URL)
