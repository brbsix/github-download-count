# -*- coding: utf-8 -*-
"""pytest setup and teardown configuration."""

# standard imports
import logging
import os
import socket
import sys

# external imports
from pytest_pylint import PyLintItem


def clean_arguments():
    """Prepare command-line args (necessary for tests involving argparse)."""
    sys.argv = ['github-download-count']


def clean_environment():
    """Unset environment variable GITHUB_TOKEN."""
    try:
        del os.environ['GITHUB_TOKEN']
    except KeyError:
        pass


def clean_logger():
    """
    Clear any pre-existing root logger configuration so that
    logging.basicConfig() can be used again.
    """
    del logging.root.handlers[:]


def disable_socket():
    """
    Monkeypatch socket to disable the Internet.
    http://stackoverflow.com/q/18601828/4117209
    """
    def guard(*args, **kwargs):  # pylint: disable=unused-argument
        """Raise an exception if socket is accessed."""
        raise RuntimeError('I told you not to use the Internet!')
    socket.socket = guard


def pytest_runtest_setup(item):
    """Setup prior to each test."""
    # skip setup for pylint tests
    if not isinstance(item, PyLintItem):
        clean_arguments()
        clean_environment()
        clean_logger()
        disable_socket()
