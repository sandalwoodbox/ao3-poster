Creating a spreadsheet
======================

You can use whatever your favorite spreadsheet application is, as long as it supports exporting to CSV (which is the format that AO3 Poster knows how to understand!)

When you're entering data into your spreadsheet, you may include any of the following columns:

+--------------------------------------+---------------------------------+
| Column header                        | Data type                       |
+======================================+=================================+
| Rating                               | ``Not Rated``,                  |
|                                      | ``General Audiences``,          |
|                                      | ``Teen And Up Audiences``,      |
|                                      | ``Mature``,                     |
|                                      | or ``Explicit``                 |
+--------------------------------------+---------------------------------+
| Archive Warnings                     | Comma-separated list of AO3     |
|                                      | archive warnings (as they       |
|                                      | appear on the New Post form.)   |
+--------------------------------------+---------------------------------+
| Fandoms                              | Comma-separated list of AO3     |
|                                      | fandom tags                     |
+--------------------------------------+---------------------------------+
| Category                             | Comma-separated list of AO3     |
|                                      | categories (as they appear      |
|                                      | on the New Post form.)          |
+--------------------------------------+---------------------------------+
| Relationships                        | Comma-separated list of AO3     |
|                                      | relationship tags               |
+--------------------------------------+---------------------------------+
| Characters                           | Comma-separated list of AO3     |
|                                      | character tags                  |
+--------------------------------------+---------------------------------+
| Additional Tags                      | Comma-separated list of tags    |
+--------------------------------------+---------------------------------+
| Work Title                           | Text                            |
+--------------------------------------+---------------------------------+
| Creator/Pseud(s)                     | Comma-separated list of AO3     |
|                                      | creator pseuds / usernames.     |
+--------------------------------------+---------------------------------+
| Summary                              | Text                            |
+--------------------------------------+---------------------------------+
| Notes at the beginning               | Text                            |
+--------------------------------------+---------------------------------+
| Notes at the end                     | Text                            |
+--------------------------------------+---------------------------------+
| This work is a remix, a translation, | URL for a work on AO3. Non-AO3  |
| a podfic, or was inspired by another | works are not currently         |
| work                                 | supported.                      |
+--------------------------------------+---------------------------------+
| Work text                            | Work HTML. *Don't include* if   |
|                                      | you want to use a work template.|
+--------------------------------------+---------------------------------+

All values included for columns must exactly match the values that AO3 expects (including capitalization) or your submission will fail.
(Or in the case of tags, it will not be tagged as you intended.)
Comma-separated values **must not** have spaces after commas.

.. image:: /_static/images/example-spreadsheet.png

You can also include additional columns; these will not be submitted to AO3 directly but they will be available in your :ref:`work text template <work-text-templates>`.