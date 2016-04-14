# -*- coding: utf-8 -*-

"""Display download counts of GitHub releases."""

from __future__ import print_function

# standard imports
import argparse
import logging
import os
import sys

# external imports
import requests

# application imports
from . import __program__, __version__


class Github(object):
    """Interact with GitHub's API."""

    def __init__(self, user=None, repo=None, tag=None, summarize=False):
        logging.basicConfig(format='%(levelname)s: %(message)s')

        self.headers = {
            'Authorization': 'token %s' % os.environ['GITHUB_TOKEN']
        } if os.environ.get('GITHUB_TOKEN') else {}

        if tag:
            self._print(self.get_releases_by_tag(user, repo, tag), summarize)
        elif repo:
            self._print(self.get_releases_by_repo(user, repo), summarize)
        else:
            self._print_all(
                self.get_releases_by_user(user if user else self.get_user()),
                summarize)

    @staticmethod
    def _print(releases, summarize=False):
        """Print download counts of releases."""
        if summarize:
            print(sum(i[1] for i in releases))
        else:
            try:
                column_width = max(len(str(d)) for n, d in releases) + 2
            except ValueError:
                sys.exit(0)
            for name, download_count in releases:
                print(str(download_count).ljust(column_width), name)

    @staticmethod
    def _print_all(all_releases, summarize=False):
        """Print download counts of all releases."""
        if summarize:
            data = []
            for repo, releases in all_releases:
                data.append((repo, sum(r[1] for r in releases)))
            try:
                column_width = max(len(str(d[1])) for d in data) + 2
            except ValueError:
                sys.exit(0)
            for repo, total in data:
                print(str(total).ljust(column_width), repo)
        else:
            try:
                column_width = max(
                    len(str(d)) for o, r in all_releases for n, d in r) + 2
            except ValueError:
                sys.exit(0)
            for repo, releases in all_releases:
                print(Terminal.BOLD + repo + Terminal.END)
                for name, download_count in releases:
                    print(str(download_count).ljust(column_width), name)
                print()

    def _request(self, url):
        """Perform a GitHub API call and return the JSON response."""
        response = requests.get('https://api.github.com' + url,
                                headers=self.headers).json()

        try:
            # message key is indicative of a malformed request
            LOG.error(response['message'])
            sys.exit(1)
        except (KeyError, TypeError):
            return response

    def get_repos_by_user(self, user):
        """Return repositories for particular user."""
        response = self._request('/users/%s/repos' % user)
        return (r['full_name'].split('/')[1] for r in response)

    def get_releases_by_repo(self, user, repo):
        """Return releases for particular repo."""
        response = self._request('/repos/%s/%s/releases' % (user, repo))
        return [(a['name'], a['download_count']) for p in response
                for a in p['assets']]

    def get_releases_by_tag(self, user, repo, tag):
        """Return releases for a particular repo tag."""
        response = self._request('/repos/%s/%s/releases/tags/%s' %
                                 (user, repo, tag))
        return [(a['name'], a['download_count']) for a in response['assets']]

    def get_releases_by_user(self, user):
        """Return releases for a particular user."""
        all_releases = []
        for repo in self.get_repos_by_user(user):
            releases = list(self.get_releases_by_repo(user, repo))
            if releases:
                all_releases.append((repo, releases))
        return all_releases

    def get_user(self):
        """Return the currently authenticated user."""
        return self._request('/user')['login']


# pylint: disable=too-few-public-methods
class Terminal(object):
    """Adjust and colorize terminal text."""
    BOLD = '\033[1m'
    END = '\033[0m'


def _parser(args):
    """Parse command-line options."""

    parser = argparse.ArgumentParser(
        add_help=False,
        description='Display download counts of GitHub releases.')

    parser.add_argument(
        'user',
        help='GitHub username',
        metavar='USER',
        nargs='?')
    parser.add_argument(
        'repo',
        help='GitHub repository',
        metavar='REPO',
        nargs='?')
    parser.add_argument(
        'tag',
        help='release tag',
        metavar='RELEASE',
        nargs='?')
    parser.add_argument(
        '-s', '--summarize',
        action='store_true',
        help='display only a total download count')

    pgroup = parser.add_argument_group('program options')
    pgroup.add_argument(
        '-h', '--help',
        action='help',
        help=argparse.SUPPRESS)
    pgroup.add_argument(
        '--version',
        action='version',
        help=argparse.SUPPRESS,
        version='%(prog)s ' + __version__)

    return parser.parse_args(args)


def main(args=None):
    """Start application."""
    options = _parser(args)
    Github(options.user, options.repo, options.tag, options.summarize)


LOG = logging.getLogger(__program__)

if __name__ == '__main__':
    main()
