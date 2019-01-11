# encoding: utf-8

import bs4
import jinja2
import requests


REQUEST_HEADERS = {
    # AO3 blocks python-requests by default so we need to fake a different user agent.
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',  # noqa: E501
}
SESSION_COOKIE_NAME = '_otwarchive_session'

LOGIN_URL = 'https://archiveofourown.org/users/login'
LOGOUT_URL = 'https://archiveofourown.org/users/logout'
# URL to post to for creating new works
POST_URL = 'https://archiveofourown.org/works'

HEADER_MAP = {
    'Rating': 'work[rating_string]',
    'Archive Warnings': 'work[warning_strings][]',
    'Fandoms': 'work[fandom_string]',
    'Category': 'work[category_string][]',
    'Relationships': 'work[relationship_string]',
    'Characters': 'work[character_string]',
    'Additional Tags': 'work[freeform_string]',
    'Work Title': 'work[title]',
    'Creator/Pseud(s)': 'pseud[byline]',
    'Summary': 'work[summary]',
    'Notes at the beginning': 'work[notes]',
    'Notes at the end': 'work[endnotes]',
    'This work is a remix, a translation, a podfic, or was inspired by another work': 'work[parent_attributes][url]',
    'Work text': 'work[chapter_attributes][content]',
}


def build_post_data(data, body_template=None):
    post_data = []

    for key, value in data.items():
        post_key = HEADER_MAP.get(key)

        if post_key is None:
            continue

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

    if body_template is not None and 'Work text' not in data:
        post_key = HEADER_MAP['Work text']
        template = jinja2.Template(body_template)
        value = template.render(data=data)
        post_data.append((
            post_key,
            value,
        ))

    return post_data


def post(session_id, data, body_template=None):
    # Takes data, posts to ao3, and returns the URL for the created work
    # or raises an exception with validation errors.
    post_data = build_post_data(data, body_template)
    requests.post(
        POST_URL,
        post_data,
        cookies={SESSION_COOKIE_NAME: session_id},
        headers=REQUEST_HEADERS,
    )


def _is_failed_login(response):
    return "The password or user name you entered doesn't match our records." in response.text


def login(username, password):
    # returns a logged-in ao3 session id or None if login failed.
    session = requests.Session()
    session.headers.update(REQUEST_HEADERS)

    response = session.get(LOGIN_URL)
    strainer = bs4.SoupStrainer(id='loginform')
    soup = bs4.BeautifulSoup(response.text, 'lxml', parse_only=strainer)
    authenticity_token = soup.find(attrs={'name': 'authenticity_token'})['value']

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
    )

    if _is_failed_login(response):
        return None

    return response.cookies[SESSION_COOKIE_NAME]


def logout(session_id):
    requests.get(
        LOGOUT_URL,
        headers=REQUEST_HEADERS,
        cookies={SESSION_COOKIE_NAME: session_id},
    )
