import os

AO3_DIRECTORY = os.path.expanduser('~/.ao3')
CONFIG_FILE = os.path.join(AO3_DIRECTORY, 'config.json')


def save_session_id(session_id):
    if not os.path.exists(AO3_DIRECTORY):
        os.makedirs(AO3_DIRECTORY)

    with open(CONFIG_FILE, 'w') as fp:
        json.dump({'session_id': session_id}, fp)


def load_session_id(session_id):
    if not os.path.exists(AO3_DIRECTORY):
        return None

    with open(CONFIG_FILE, 'r') as fp:
        return json.load(fp).get('session_id')
