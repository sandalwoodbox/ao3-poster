# ao3-poster [![Build Status](https://travis-ci.org/melinath/ao3-poster.svg?branch=master)](https://travis-ci.org/melinath/ao3-poster)

This python package exists to make posting to ao3 simpler.
The goal is to allow people to have a single source-of-truth document which is easy to edit, then batch-upload items from that document to ao3.

## Using ao3-poster

These instructions assume that you're using Mac OS X or Linux.
This will not work the same way on Windows.

Install ao3-poster:

```
pip install ao3-poster
```

### Downloading data from a google sheet

It is easiest at this time to download sheets as CSVs using the Google Sheets web interface.

If you instead want to use ao3-poster to download csvs of google sheets,
you will need to set up Google service application credentials.
Follow the instructions here: https://cloud.google.com/docs/authentication/getting-started
You only need to do the "Creating a service account" and "Setting the environment variable" sections.
You will also need to enable the "Sheets" API for the credentials you create; the easiest way to do this will be to try to run an ao3-poster command and then use the link in the error message.

You may then run:

```
ao3 get-sheet <sheet_id> data.csv
```

### Uploading a CSV

Once you have a data csv, you can upload it to ao3 using:

```
ao3 post data.csv --body-template=body_template.html
```

The `--body-template` option can take a jinja2 template file, which will be rendered as the work content for each row using the data provided in the csv.


## Developing ao3-poster

### Requirements
Install pipenv: https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv

### Setting up
```bash
git clone git@github.com:melinath/ao3-poster.git
cd ao3-poster
pipenv install
pipenv shell
python setup.py develop
```

### Running tests
```bash
python setup.py test
```

### Running isort
This may be necessary to resolve isort flake8 errors.

```bash
pipenv shell
pip install .[flake8]
isort -rc
```
