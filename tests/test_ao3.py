from ao3_poster.ao3 import HEADER_MAP
from ao3_poster.ao3 import build_post_data


def test_build_post_data__handles_single_values():
    data = {
        'Rating': 'Not Rated',
    }
    post_data = build_post_data(data)
    assert post_data == [
        (HEADER_MAP['Rating'], 'Not Rated'),
    ]


def test_build_post_data__handles_multivalues__single_value():
    data = {
        'Archive Warnings': 'Graphic Depictions Of Violence',
    }
    post_data = build_post_data(data)
    assert post_data == [
        (HEADER_MAP['Archive Warnings'], 'Graphic Depictions Of Violence'),
    ]


def test_build_post_data__handles_multivalues__multiple_values():
    data = {
        'Archive Warnings': 'Graphic Depictions Of Violence, Major Character Death',
    }
    post_data = build_post_data(data)
    assert post_data == [
        (HEADER_MAP['Archive Warnings'], 'Graphic Depictions Of Violence'),
        (HEADER_MAP['Archive Warnings'], 'Major Character Death'),
    ]
