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


def test_build_post_data__handles_empty_data():
    post_data = build_post_data({})
    assert post_data == []


def test_build_post_data__handles_unmapped_keys():
    post_data = build_post_data({
        'Extra field': 'value',
    })
    assert post_data == []


def test_build_post_data__formats_body_text():
    post_data = build_post_data({
        'Extra field': 'value',
    }, body_template='{{ data["Extra field"] }}')
    assert post_data == [
        (HEADER_MAP['Work text'], 'value')
    ]


def test_build_post_data__prefers_explicit_work_text():
    post_data = build_post_data({
        'Work text': 'foobar',
        'Extra field': 'value',
    }, body_template='{{ data["Extra field"] }}')
    assert post_data == [
        (HEADER_MAP['Work text'], 'foobar')
    ]
