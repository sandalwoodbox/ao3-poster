.. _work-text-templates:

Work Text Templates
===================

If you don't specify a "Work Text" column in your :ref:`spreadsheet <creating-a-spreadsheet>` you have the option of using a template instead.
AO3 Poster uses `Jinja2 Templates`_.

.. _Jinja2 Templates: http://jinja.pocoo.org/docs/2.10/

Your spreadsheet data will be available in the template as ``data``.
For example, if your spreadsheet has an optional ``Length`` column for podcast length, your template might look like this:

.. code-block:: jinja

   <p>Thanks for listening to {{ data['Work Title'] }}!</p>
   {% if data['Length'] %}<p><strong>Length:</strong> {{ data['Length'] }}</p>{% endif %}

Code editors
------------

For editing your work text template, it is **critical** that you use a code editor like `Sublime Text`_.
Text editors like TextEdit or Word will insert invisible formatting marks into your template that may prevent it from rendering or make it render differently than you would expect.
Code editors also have the ability to provide syntax highlighting to make it easier to read your template.

.. _Sublime Text: https://www.sublimetext.com/
