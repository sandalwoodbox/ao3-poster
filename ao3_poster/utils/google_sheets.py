try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping

from googleapiclient.discovery import build


class Row(MutableMapping):
    def __init__(self, headers, row, index):
        self.data = dict(zip(headers, row))
        self.index = index

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return self.data.__len__()

    def __repr__(self):
        return self.data.__repr__()


def get_sheet_data(sheet_id, count):
    service = build('sheets', 'v4')
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range='A1:ZZ{}'.format(count + 1),
    ).execute()
    rows = result.get('values', [])
    headers = rows[0]
    return headers, [
        Row(headers, row, index + 1)
        for index, row in enumerate(rows[1:])
    ]
