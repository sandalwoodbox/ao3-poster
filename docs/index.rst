Welcome to AO3 Poster's documentation!
======================================

AO3 Poster was originally designed for podficcers who are trying to upload a backlog of podfic to AO3 that had previously been hosted on other services.
Its focus is therefore on bulk posting data from spreadsheets to AO3 and templating of work text (for cover art, media players, etc.)

.. note:: AO3 Poster is only "officially" expected to work on Mac and Linux computers. It may or may not work on Windows.

Using the command line
----------------------

AO3 Poster is a command line tool.
If you are not familiar with the command line, please read `Introduction to the command-line interface <https://tutorial.djangogirls.org/en/intro_to_command_line/>`_ and/or watch `Your new friend: Command Line <https://www.youtube.com/watch?v=jvZLWhkzX-8>`_ before using AO3 Poster.

Installing Python
-----------------

AO3 Poster uses the programming language ``Python``.
You will need to install Python on your computer to use AO3 Poster.
You can follow the instructions at `Let’s start with Python <https://tutorial.djangogirls.org/en/python_installation/>`_ and/or watch `Installing Python & Code Editor <https://www.youtube.com/watch?v=pVTaqzKZCdA>`_.

If you have a terminal window open, close it and open a new one so that the python installation can take full effect.

Installing AO3 Poster
---------------------

Once you have python installed, you're ready to install AO3 Poster!
The instructions below assume you installed Python using the method described above:

.. code-block:: bash

   $ pip3 install ao3-poster

If you ever want to get a new version of ao3-poster, you can use:

.. code-block:: bash

   $ pip3 install -U ao3-poster

Posting to AO3
--------------

Once AO3 Poster is installed, you can post to AO3 by doing either of the following commands:

.. code-block:: bash

   $ ao3 post ~/Desktop/data.csv
   $ ao3 post ~/Desktop/data.csv --work-text-template=~/Desktop/work_text_template.html

Be sure to replace the example paths with the real paths to your ``csv`` and ``work_text_template.html`` files.
See :ref:`creating-a-spreadsheet` and :ref:`work-text-templates` for more information about setting up those files.


.. toctree::
   :maxdepth: 1

   creating-a-spreadsheet
   work-text-templates
   contributing-code
