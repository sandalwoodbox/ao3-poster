from ao3_poster.ao3 import HEADER_MAP
from ao3_poster.ao3 import build_post_data
from ao3_poster.ao3 import get_validation_errors


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
      <p title="try again">
        <input class="autocomplete" autocomplete_method="/autocomplete/pseud" autocomplete_hint_text="Start typing for suggestions!" autocomplete_no_results_text="(No suggestions found)" autocomplete_min_chars="1" autocomplete_searching_text="Searching..." size="50" type="text" name="pseud[byline]" id="pseud_byline">
      </p>
      <!-- expects a local variable "form" -->
    </form>
    """
    validation_errors = get_validation_errors(html)
    assert validation_errors == [
        'Invalid pseuds listed as authors',
    ]


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
