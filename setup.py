#!/usr/bin/env python3

"""Test, build, or install the PyMosaic package.

Run tests:
  python setup.py test

Build and install:
  python setup.py build && python setup.py install
"""

from distutils.util import convert_path
from setuptools import setup, find_packages

VER_FILEPATH = convert_path('pymosaic/version.txt')
with open(VER_FILEPATH) as file:
    __version__ = file.read()

setup(
    name='PyMosaic',
    description='A mosaic generating program',
    url='https://github.com/texruska/PyMosaic',
    author='Steven Burnett',
    author_email='texruska@users.noreply.github.com',
    license='GPLv3',
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=[
        'coverage',
        'pytest',
        'pytest-cov',
        'pytest-pylint'
    ],
    version=__version__,
)
