import jinja2
import pytest

from ao3_poster.ao3 import HEADER_MAP
from ao3_poster.ao3 import build_post_data
from ao3_poster.ao3 import get_pseuds
from ao3_poster.ao3 import get_validation_errors
from ao3_poster.exceptions import ValidationError


def test_get_validation_errors__no_errors():
    html = ""
    validation_errors = get_validation_errors(html)
    assert validation_errors == []


def test_get_validation_errors__with_form_errors():
    html = """
    <div id="error" class="error">
        <h4>Sorry! We couldn't save this work because:</h4>
        <ul>
            <li>Please enter your story in the text field below.</li>
        </ul>
    </div>
    """
    validation_errors = get_validation_errors(html)
    assert validation_errors == [
        'Please enter your story in the text field below.',
    ]


def test_get_validation_errors__with_invalid_pseuds():
    html = """
    <form class="new_work" id="new_work" action="/works" accept-charset="UTF-8" method="post">
      <!-- expects a local variable "form" -->
      <h4 class="heading">These pseuds are invalid: </h4>
      <ul>
        <li>sandalwoodbox</li>
      </ul>
      <p><label for="work_pseud">Try again:</label></p>
      <!-- expects a local variable "form" -->
    </form>
    """
    validation_errors = get_validation_errors(html)
    assert validation_errors == [
        'Invalid pseuds listed as authors',
    ]


def test_get_pseuds__one():
    html = """
    <select name="work[author_attributes][ids][]" id="work_author_attributes_ids_" multiple="multiple">
        <option selected="selected" value="42">test</option>
    </select>
    """
    pseuds = get_pseuds(html)
    assert pseuds == {
        'test': '42',
    }


def test_get_pseuds__multiple():
    html = """
    <select name="work[author_attributes][ids][]" id="work_author_attributes_ids_" multiple="multiple">
        <option selected="selected" value="42">test</option>
        <option value="44">test2</option>
    </select>
    """
    pseuds = get_pseuds(html)
    assert pseuds == {
        'test': '42',
        'test2': '44',
    }


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
    }, work_text_template=jinja2.Template('{{ data["Extra field"] }}'))
    assert post_data == [
        (HEADER_MAP['Work text'], 'value')
    ]


def test_build_post_data__prefers_explicit_work_text():
    post_data = build_post_data({
        'Work text': 'foobar',
        'Extra field': 'value',
    }, work_text_template=jinja2.Template('{{ data["Extra field"] }}'))
    assert post_data == [
        (HEADER_MAP['Work text'], 'foobar')
    ]


def test_build_post_data__handles_pseuds__single():
    post_data = build_post_data(
        data={
            'Creator/Pseud(s)': 'test',
        },
        pseuds={
            'test': '42',
        },
    )
    assert post_data == [
        (HEADER_MAP['Creator/Pseud(s)'], '42'),
    ]


def test_build_post_data__handles_pseuds__multiple():
    post_data = build_post_data(
        data={
            'Creator/Pseud(s)': 'test,test2',
        },
        pseuds={
            'test': '42',
            'test2': '43',
        },
    )
    assert post_data == [
        (HEADER_MAP['Creator/Pseud(s)'], '42'),
        (HEADER_MAP['Creator/Pseud(s)'], '43'),
    ]


def test_build_post_data__handles_pseuds__incorrect():
    with pytest.raises(ValidationError):
        build_post_data(
            data={
                'Creator/Pseud(s)': 'test,test2',
            },
            pseuds={
                'test': '42',
            },
        )
