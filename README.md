ao3-poster
==========

This python package exists to make posting to ao3 simpler.
The goal is to allow people to have a single source-of-truth document which is easy to edit, then batch-upload items from that document to ao3.

Requirements
------------
Install pipenv: https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv

Setting up
-----------
```bash
git clone git@github.com:sandalwoodbox/ao3-poster.git
cd ao3-poster
pipenv install
pipenv shell
python setup.py develop
```

Running tests
-------------
```bash
python setup.py test
```

Running isort
-------------
This may be necessary to resolve isort flake8 errors.

```bash
pipenv shell
pip install .[flake8]
isort -rc
```
