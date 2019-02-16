.. _contributing-code:

Contributing code to ao3-poster
===============================

Contributions are welcome! The github repository is at https://github.com/melinath/ao3-poster.

Requirements
++++++++++++

Install pipenv: https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv

Setting up
++++++++++

.. code-block:: bash

   $ git clone git@github.com:melinath/ao3-poster.git
   $ cd ao3-poster
   $ pipenv install
   $ pipenv shell
   $ python setup.py develop


Running tests
+++++++++++++

.. code-block:: bash

   $ pipenv shell
   $ python setup.py test

Running isort
+++++++++++++

This may be necessary to resolve isort flake8 errors.

.. code-block:: bash

   $ pipenv shell
   $ pip install .[flake8]
   $ isort -rc
