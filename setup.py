#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import Command
from setuptools import find_packages
from setuptools import setup
from setuptools.command.test import test as TestCommand


# Package meta-data.
NAME = 'ao3-poster'
SRC_DIR = 'ao3_poster'
DESCRIPTION = 'Automatically post to ao3'
URL = 'https://github.com/melinath/ao3-poster'
EMAIL = 'stephen.r.burrows@gmail.com'
AUTHOR = 'Stephen Burrows'
REQUIRES_PYTHON = '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    'beautifulsoup4>=4.7.1',
    'click>=7.0',
    'google-api-python-client>=1.7.7',
    'jinja2==2.11.3',
    'lxml>=4.3.0',
    'requests>=2.21.0',
]

# What packages are required only for tests?
TESTS = [
    'pytest>=3.8.0',
    'pytest-mock>=1.10.0',
    'mock>=2.0.0',
    'more-itertools<6.0.0',
]

# What packages are optional?
EXTRAS = {
    'flake8': [
        'flake8>=3.5.0',
        'flake8-isort>=2.5',
        'isort>=4.3.4',
        'testfixtures>=6.3.0',
    ],
    'docs': [
        'sphinx>=1.8.4',
    ],
}

here = os.path.abspath(os.path.dirname(__file__))

try:
    # Python 3 will raise FileNotFoundError instead of IOError
    FileNotFoundError = IOError
except NameError:
    pass

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in the MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, SRC_DIR, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag {0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),

    entry_points={
        'console_scripts': ['ao3=ao3_poster.cli:cli'],
    },
    install_requires=REQUIRED,
    tests_require=TESTS,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    # $ setup.py publish support.
    cmdclass={
        'pytest': PyTest,
        'upload': UploadCommand,
    },
)
