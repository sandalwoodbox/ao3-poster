import jinja2
import pytest

from ao3_poster.ao3 import HEADER_MAP
from ao3_poster.ao3 import build_post_data
from ao3_poster.ao3 import get_languages
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


def test_get_languages():
    html = """
    <select id="work_language_id" name="work[language_id]">
        <option selected="selected" value="73">Afrikaans</option>
    </select>
    """
    languages = get_languages(html)
    assert languages == {
        'Afrikaans': '73',
    }


def test_get_languages__excludes_select_a_language():
    html = """
    <select id="work_language_id" name="work[language_id]">
        <option value="">Please select a language</option>
    </select>
    """
    languages = get_languages(html)
    assert languages == {}


def test_build_post_data__handles_single_values():
    data = {
        'Rating': 'Not Rated',
    }
    post_data = build_post_data(
        data=data,
        pseuds={},
        languages={},
    )
    assert post_data == [
        (HEADER_MAP['Rating'], 'Not Rated'),
    ]


def test_build_post_data__handles_multivalues__single_value():
    data = {
        'Archive Warnings': 'Graphic Depictions Of Violence',
    }
    post_data = build_post_data(
        data=data,
        pseuds={},
        languages={},
    )
    assert post_data == [
        (HEADER_MAP['Archive Warnings'], 'Graphic Depictions Of Violence'),
    ]


def test_build_post_data__handles_multivalues__multiple_values():
    data = {
        'Archive Warnings': 'Graphic Depictions Of Violence, Major Character Death',
    }
    post_data = build_post_data(
        data=data,
        pseuds={},
        languages={},
    )
    assert post_data == [
        (HEADER_MAP['Archive Warnings'], 'Graphic Depictions Of Violence'),
        (HEADER_MAP['Archive Warnings'], 'Major Character Death'),
    ]


def test_build_post_data__handles_empty_data():
    post_data = build_post_data(
        data={},
        pseuds={},
        languages={},
    )
    assert post_data == []


def test_build_post_data__handles_unmapped_keys():
    post_data = build_post_data(
        data={
            'Extra field': 'value',
        },
        pseuds={},
        languages={},
    )
    assert post_data == []


def test_build_post_data__formats_body_text():
    post_data = build_post_data(
        data={
            'Extra field': 'value',
        },
        pseuds={},
        languages={},
        work_text_template=jinja2.Template('{{ data["Extra field"] }}'),
    )
    assert post_data == [
        (HEADER_MAP['Work text'], 'value')
    ]


def test_build_post_data__prefers_explicit_work_text():
    post_data = build_post_data(
        data={
            'Work text': 'foobar',
            'Extra field': 'value',
        },
        pseuds={},
        languages={},
        work_text_template=jinja2.Template('{{ data["Extra field"] }}'),
    )
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
        languages={},
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
        languages={},
    )
    assert post_data == [
        (HEADER_MAP['Creator/Pseud(s)'], '42'),
        (HEADER_MAP['Creator/Pseud(s)'], '43'),
    ]


def test_build_post_data__handles_pseuds__invalid():
    with pytest.raises(ValidationError):
        build_post_data(
            data={
                'Creator/Pseud(s)': 'test,test2',
            },
            pseuds={
                'test': '42',
            },
            languages={},
        )


def test_build_post_data__handles_language():
    post_data = build_post_data(
        data={
            'Language': 'English',
        },
        pseuds={},
        languages={
            'English': '100',
        },
    )
    assert post_data == [
        (HEADER_MAP['Language'], '100'),
    ]


def test_build_post_data__handles_language__invalid():
    with pytest.raises(ValidationError):
        build_post_data(
            data={
                'Language': 'English',
            },
            pseuds={},
            languages={},
        )


def test_build_post_data__returns_all_errors():
    with pytest.raises(ValidationError) as excinfo:
        build_post_data(
            data={
                'Creator/Pseud(s)': 'test,test2',
                'Language': 'English',
            },
            pseuds={},
            languages={},
        )

    error_message = str(excinfo.value)
    assert 'The following are not your pseuds' in error_message
    assert 'Unknown language' in error_message
