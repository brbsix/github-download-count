# -*- coding: utf-8 -*-

"""
Application setup script

To build package:
python3 setup.py sdist bdist_wheel clean

To run tests in an virtualenv:
python3 setup.py test

To run tests directly with verbose output:
python3 -m pytest -vv
"""

# Python 2 forwards-compatibility
from __future__ import absolute_import

# standard imports
import os

# external imports
from setuptools import setup

# application imports
from gdc import __description__, __program__, __version__


def read(path):
    """Convert Markdown to reStructuredText if possible."""
    with open(path) as file_object:
        text = file_object.read()

    try:
        import pypandoc
        return pypandoc.convert(text, 'rst', 'md')
    except ImportError:
        return text


# allow setup.py to be run from any path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SETUP_REQUIRES = ['pytest-runner']
INSTALL_REQUIRES = ['requests']
TESTS_REQUIRE = ['pytest-cov', 'pytest-pylint', 'requests_mock']

# install standalone mock if necessary (Python 2.7)
try:
    __import__('unittest.mock')
except ImportError:
    TESTS_REQUIRE.append('mock')

setup(
    name=__program__,
    version=__version__,
    description=__description__,
    author='Brian Beffa',
    author_email='brbsix@gmail.com',
    long_description=read('README.md'),
    url='https://github.com/brbsix/github-download-count',
    license='GPLv3',
    keywords=['GitHub', 'API', 'release', 'download', 'count'],
    packages=['gdc'],
    install_requires=INSTALL_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require={'testing': TESTS_REQUIRE},
    entry_points={
        'console_scripts': ['github-download-count=gdc.gdc:main'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities'
    ]
)
