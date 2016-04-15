# -*- coding: utf-8 -*-
# pylint: disable=invalid-name,no-init,no-self-use,old-style-class,protected-access,redefined-outer-name,too-few-public-methods

"""Tests for gdc.py"""

# standard imports
import argparse
import hashlib
import json
import os
from textwrap import dedent
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# external imports
import pytest
import requests_mock

# application imports
from gdc import gdc


###############
# CLASS TESTS #
###############

class TestGithubInit:
    """Test Github.__init__."""

    def test_init_no_token(self):
        """Test for no authorization token (GITHUB_TOKEN unset)."""
        assert gdc.Github().headers == {}

    def test_init_with_token(self, token_valid):
        """Test for authorization token (GITHUB_TOKEN set)."""
        assert gdc.Github().headers == {
            'Authorization': 'token %s' % token_valid
        }

    # pylint: disable=unused-argument
    def test_init_empty_token(self, token_empty):
        """Test for empty authorization token (GITHUB_TOKEN set empty)."""
        assert gdc.Github().headers == {}


class TestGithubPrivate:
    """Test Github class private functions."""

    def test_get(self):
        """Test _get method."""
        api = '/users/brbsix'
        url = 'https://api.github.com' + api
        text = (
            '{"login":"brbsix"'
            ',"id":6672131'
            ',"avatar_url":"https://avatars.githubusercontent.com/u/6672131?v=3"'
            ',"gravatar_id":"","url":"https://api.github.com/users/brbsix"'
            ',"html_url":"https://github.com/brbsix"'
            ',"followers_url":"https://api.github.com/users/brbsix/followers"'
            ',"following_url":"https://api.github.com/users/brbsix/following{/other_user}"'
            ',"gists_url":"https://api.github.com/users/brbsix/gists{/gist_id}"'
            ',"starred_url":"https://api.github.com/users/brbsix/starred{/owner}{/repo}"'
            ',"subscriptions_url":"https://api.github.com/users/brbsix/subscriptions"'
            ',"organizations_url":"https://api.github.com/users/brbsix/orgs"'
            ',"repos_url":"https://api.github.com/users/brbsix/repos"'
            ',"events_url":"https://api.github.com/users/brbsix/events{/privacy}"'
            ',"received_events_url":"https://api.github.com/users/brbsix/received_events"'
            ',"type":"User"'
            ',"site_admin":false'
            ',"name":"Six"'
            ',"company":null'
            ',"blog":"https://brbsix.github.com"'
            ',"location":"SF Bay Area"'
            ',"email":null'
            ',"hireable":true'
            ',"bio":null'
            ',"public_repos":51'
            ',"public_gists":7'
            ',"followers":14'
            ',"following":85'
            ',"created_at":"2014-02-13T12:50:01Z"'
            ',"updated_at":"2016-04-10T04:55:45Z"}'
        )

        with requests_mock.Mocker() as mock:
            mock.get(url, text=text)

            assert gdc.Github()._get(api) == json.loads(text)

    def test_request_with_invalid_response(self, capfd):
        """Test _request method with an invalid response."""
        api = '/badrequest'
        url = 'https://api.github.com' + api
        text = (
            '{"message":"Not Found"'
            ',"documentation_url":"https://developer.github.com/v3"}'
        )

        with requests_mock.Mocker() as mock:
            mock.get(url, text=text)

            with pytest.raises(SystemExit) as exception:
                # perform request
                gdc.Github()._request(api)

        # ensure stderr and exit status are as expected
        assert capfd.readouterr()[1] == 'ERROR: Not Found\n' and \
            exception.value.code is 1

    def test_request_with_invalid_token(self, capfd, token_invalid):
        """Test _request method with an invalid authentication token."""
        api = '/user'
        url = 'https://api.github.com' + api
        text = (
            '{"message":"Bad credentials"'
            ',"documentation_url":"https://developer.github.com/v3"}'
        )
        request_headers = {'Authorization': 'token %s' % token_invalid}

        with requests_mock.Mocker() as mock:
            mock.get(url, request_headers=request_headers, text=text)

            with pytest.raises(SystemExit) as exception:
                # perform request
                gdc.Github()._request(api)

        # ensure stderr and exit status are as expected
        assert capfd.readouterr()[1] == 'ERROR: Bad credentials\n' \
            and exception.value.code is 1

    def test_request_with_no_token(self, capfd):
        """Test _request method with no authentication token."""
        api = '/user'
        url = 'https://api.github.com' + api
        text = (
            '{"message":"Requires authentication"'
            ',"documentation_url":"https://developer.github.com/v3"}'
        )

        with requests_mock.Mocker() as mock:
            mock.get(url, text=text)

            with pytest.raises(SystemExit) as exception:
                # perform request
                gdc.Github()._request(api)

        # ensure stderr and exit status are as expected
        assert capfd.readouterr()[1] == 'ERROR: Requires authentication\n' \
            and exception.value.code is 1

    def test_request_with_valid_response(self):
        """Test _request method with a valid response."""
        api = '/users/brbsix'
        url = 'https://api.github.com' + api
        text = (
            '{"login":"brbsix"'
            ',"id":6672131'
            ',"avatar_url":"https://avatars.githubusercontent.com/u/6672131?v=3"'
            ',"gravatar_id":"","url":"https://api.github.com/users/brbsix"'
            ',"html_url":"https://github.com/brbsix"'
            ',"followers_url":"https://api.github.com/users/brbsix/followers"'
            ',"following_url":"https://api.github.com/users/brbsix/following{/other_user}"'
            ',"gists_url":"https://api.github.com/users/brbsix/gists{/gist_id}"'
            ',"starred_url":"https://api.github.com/users/brbsix/starred{/owner}{/repo}"'
            ',"subscriptions_url":"https://api.github.com/users/brbsix/subscriptions"'
            ',"organizations_url":"https://api.github.com/users/brbsix/orgs"'
            ',"repos_url":"https://api.github.com/users/brbsix/repos"'
            ',"events_url":"https://api.github.com/users/brbsix/events{/privacy}"'
            ',"received_events_url":"https://api.github.com/users/brbsix/received_events"'
            ',"type":"User"'
            ',"site_admin":false'
            ',"name":"Six"'
            ',"company":null'
            ',"blog":"https://brbsix.github.com"'
            ',"location":"SF Bay Area"'
            ',"email":null'
            ',"hireable":true'
            ',"bio":null'
            ',"public_repos":51'
            ',"public_gists":7'
            ',"followers":14'
            ',"following":85'
            ',"created_at":"2014-02-13T12:50:01Z"'
            ',"updated_at":"2016-04-10T04:55:45Z"}'
        )

        with requests_mock.Mocker() as mock:
            mock.get(url, text=text)

            assert gdc.Github()._request(api) == json.loads(text)


class TestGithubGetReposByUser:
    """Test Github class get_repos_by_user method."""

    def test_get_repos_by_user(self):
        """Test get_repos_by_user method."""
        repos_wanted = [
            'android_frameworks_base', 'aria2-webui-launcher', 'bart',
            'bash-config', 'brackets', 'brackets-shell', 'brbsix.github.io',
            'broadway-scripts', 'caffeine-reloaded', 'cookiecutter-pylibrary',
            'craigslist-rental-market', 'debtool', 'deepdiff', 'devscripts',
            'dlocate', 'dockerize', 'dpkg-repack', 'DuckieTV-installer',
            'encfs-tool', 'github-download-count', 'icon-library', 'imgur.sh',
            'installdist', 'minidb', 'net-utils', 'notify-ssh', 'periscope',
            'ping-indicator', 'piptool', 'ppa-tools'
        ]

        with requests_mock.Mocker() as mock:
            mock.get('https://api.github.com/users/brbsix/repos',
                     text=read('repos'))
            repos = list(gdc.Github().get_repos_by_user('brbsix'))

        assert repos == repos_wanted


class TestGithubGetReleasesByRepo:
    """Test Github class get_releases_by_repo method."""

    def test_get_releases_by_repo(self):
        """Test get_releases_by_repo method."""
        releases_wanted = [
            ('debtool_0.2.5_all.deb', 62),
            ('debtool_0.2.4_all.deb', 5),
            ('debtool_0.2.1_all.deb', 0),
            ('debtool_0.2.2_all.deb', 0),
            ('debtool_0.2.3_all.deb', 2)
        ]

        with requests_mock.Mocker() as mock:
            mock.get('https://api.github.com/repos/brbsix/debtool/releases',
                     text=read('debtool_releases'))
            releases = list(
                gdc.Github().get_releases_by_repo('brbsix', 'debtool')
            )

        assert releases == releases_wanted

    def test_get_releases_by_repo_for_repo_without_releases(self):
        """Test get_releases_by_repo method for a repo without any releases."""
        with requests_mock.Mocker() as mock:
            mock.get('https://api.github.com/repos/brbsix/craigslist/releases',
                     text='[]')
            releases = list(
                gdc.Github().get_releases_by_repo('brbsix', 'craigslist')
            )

        assert releases == []


class TestGithubGetReleasesByTag:
    """Test Github class get_releases_by_tag method."""

    def test_get_releases_by_tag(self):
        """Test get_releases_by_tag method."""
        releases_wanted = [('debtool_0.2.5_all.deb', 62)]

        with requests_mock.Mocker() as mock:
            mock.get('https://api.github.com/repos/brbsix/debtool/releases/tags/v0.2.5',
                     text=read('tag'))
            releases = list(
                gdc.Github().get_releases_by_tag(
                    'brbsix', 'debtool', 'v0.2.5'
                )
            )

        assert releases == releases_wanted

    def test_get_releases_by_tag_for_repo_without_assets(self):
        """
        Test get_releases_by_tag method for a repo without any downloadable
        binary assets.
        """
        with requests_mock.Mocker() as mock:
            mock.get('https://api.github.com/repos/fopina/pyspeedtest/releases/tags/v1.2.4',
                     text=read('tag_empty'))
            releases = list(
                gdc.Github().get_releases_by_tag(
                    'fopina', 'pyspeedtest', 'v1.2.4'
                )
            )

        assert releases == []


class TestGithubGetReleasesByUser:
    """Test Github class get_releases_by_user method."""

    def test_get_releases_by_user(self):
        """Test get_releases_by_user method."""
        # repos used to create mocks
        repos = [
            'android_frameworks_base', 'aria2-webui-launcher', 'bart',
            'bash-config', 'brackets', 'brackets-shell', 'brbsix.github.io',
            'broadway-scripts', 'cookiecutter-pylibrary',
            'craigslist-rental-market', 'deepdiff', 'devscripts', 'dlocate',
            'dockerize', 'dpkg-repack', 'DuckieTV-installer', 'encfs-tool',
            'github-download-count', 'icon-library', 'imgur.sh', 'installdist',
            'minidb', 'net-utils', 'notify-ssh', 'periscope', 'ping-indicator',
            'piptool', 'ppa-tools'
        ]
        mocks = [
            ('https://api.github.com/users/brbsix/repos',
             read('repos')),
            ('https://api.github.com/repos/brbsix/caffeine-reloaded/releases',
             read('caffeine_releases')),
            ('https://api.github.com/repos/brbsix/debtool/releases',
             read('debtool_releases'))
        ]
        for repo in repos:
            mocks.append(('https://api.github.com/repos/brbsix/%s/releases' % repo, '[]'))

        releases_wanted = [
            ('caffeine-reloaded', [
                ('caffeine-reloaded_0.0.3_all.deb', 2),
                ('caffeine-reloaded_0.0.2_all.deb', 1),
                ('caffeine-reloaded_0.0.1_all.deb', 0)
            ]),
            ('debtool', [
                ('debtool_0.2.5_all.deb', 62),
                ('debtool_0.2.4_all.deb', 5),
                ('debtool_0.2.1_all.deb', 0),
                ('debtool_0.2.2_all.deb', 0),
                ('debtool_0.2.3_all.deb', 2)
            ])
        ]

        with requests_mock.Mocker() as mock:
            # set up mocks
            for url, text in mocks:
                mock.get(url, text=text)
            releases = list(gdc.Github().get_releases_by_user('brbsix'))

        assert releases == releases_wanted


class TestGithubGetUser:
    """Test Github class get_user method."""

    def test_get_user(self, token_valid):
        """Test get_user method (requires authentication token)."""
        url = 'https://api.github.com/user'
        text = (
            '{"login":"brbsix"'
            ',"id":6672131'
            ',"avatar_url":"https://avatars.githubusercontent.com/u/6672131?v=3"'
            ',"gravatar_id":"","url":"https://api.github.com/users/brbsix"'
            ',"html_url":"https://github.com/brbsix"'
            ',"followers_url":"https://api.github.com/users/brbsix/followers"'
            ',"following_url":"https://api.github.com/users/brbsix/following{/other_user}"'
            ',"gists_url":"https://api.github.com/users/brbsix/gists{/gist_id}"'
            ',"starred_url":"https://api.github.com/users/brbsix/starred{/owner}{/repo}"'
            ',"subscriptions_url":"https://api.github.com/users/brbsix/subscriptions"'
            ',"organizations_url":"https://api.github.com/users/brbsix/orgs"'
            ',"repos_url":"https://api.github.com/users/brbsix/repos"'
            ',"events_url":"https://api.github.com/users/brbsix/events{/privacy}"'
            ',"received_events_url":"https://api.github.com/users/brbsix/received_events"'
            ',"type":"User"'
            ',"site_admin":false'
            ',"name":"Six"'
            ',"company":null'
            ',"blog":"https://brbsix.github.com"'
            ',"location":"SF Bay Area"'
            ',"email":null'
            ',"hireable":true'
            ',"bio":null'
            ',"public_repos":51'
            ',"public_gists":7'
            ',"followers":14'
            ',"following":85'
            ',"created_at":"2014-02-13T12:50:01Z"'
            ',"updated_at":"2016-04-10T04:55:45Z"}'
        )
        request_headers = {'Authorization': 'token %s' % token_valid}

        with requests_mock.Mocker() as mock:
            mock.get(url, request_headers=request_headers, text=text)

            assert gdc.Github().get_user() == 'brbsix'


class TestGithubShow:
    """Test Github class show method."""

    def test_show_with_user(self, capfd):
        """Test show method with user."""
        data = [
            ('caffeine-reloaded', [
                ('caffeine-reloaded_0.0.3_all.deb', 2),
                ('caffeine-reloaded_0.0.2_all.deb', 1),
                ('caffeine-reloaded_0.0.1_all.deb', 0)
            ]),
            ('debtool', [
                ('debtool_0.2.5_all.deb', 62),
                ('debtool_0.2.4_all.deb', 5),
                ('debtool_0.2.1_all.deb', 0),
                ('debtool_0.2.2_all.deb', 0),
                ('debtool_0.2.3_all.deb', 2)
            ])
        ]
        text_wanted = (
            '\x1b[1mcaffeine-reloaded\x1b[0m\n'
            '2    caffeine-reloaded_0.0.3_all.deb\n'
            '1    caffeine-reloaded_0.0.2_all.deb\n'
            '0    caffeine-reloaded_0.0.1_all.deb\n'
            '\n'
            '\x1b[1mdebtool\x1b[0m\n'
            '62   debtool_0.2.5_all.deb\n'
            '5    debtool_0.2.4_all.deb\n'
            '0    debtool_0.2.1_all.deb\n'
            '0    debtool_0.2.2_all.deb\n'
            '2    debtool_0.2.3_all.deb\n'
            '\n'
        )

        github = gdc.Github()
        with patch.object(github, 'get_releases_by_user') as mocked_function:
            mocked_function.return_value = data
            github.get_releases_by_user = mocked_function
            github.show('brbsix')

        mocked_function.assert_called_once_with('brbsix')
        assert capfd.readouterr()[0] == text_wanted

    def test_show_with_user_summarized(self, capfd):
        """Test show method with user (summarized)."""
        data = [
            ('caffeine-reloaded', [
                ('caffeine-reloaded_0.0.3_all.deb', 2),
                ('caffeine-reloaded_0.0.2_all.deb', 1),
                ('caffeine-reloaded_0.0.1_all.deb', 0)
            ]),
            ('debtool', [
                ('debtool_0.2.5_all.deb', 62),
                ('debtool_0.2.4_all.deb', 5),
                ('debtool_0.2.1_all.deb', 0),
                ('debtool_0.2.2_all.deb', 0),
                ('debtool_0.2.3_all.deb', 2)
            ])
        ]
        text_wanted = dedent('''\
            3    caffeine-reloaded
            69   debtool
            ''')

        github = gdc.Github()
        with patch.object(github, 'get_releases_by_user') as mocked_function:
            mocked_function.return_value = data
            github.get_releases_by_user = mocked_function
            github.show('brbsix', summarize=True)

        mocked_function.assert_called_once_with('brbsix')
        assert capfd.readouterr()[0] == text_wanted

    def test_show_with_repo(self, capfd):
        """Test show method with repo."""
        data = [('debtool_0.2.5_all.deb', 62),
                ('debtool_0.2.4_all.deb', 5),
                ('debtool_0.2.1_all.deb', 0),
                ('debtool_0.2.2_all.deb', 0),
                ('debtool_0.2.3_all.deb', 2)]
        text_wanted = dedent('''\
            62   debtool_0.2.5_all.deb
            5    debtool_0.2.4_all.deb
            0    debtool_0.2.1_all.deb
            0    debtool_0.2.2_all.deb
            2    debtool_0.2.3_all.deb
            ''')

        github = gdc.Github()
        with patch.object(github, 'get_releases_by_repo') as mocked_function:
            mocked_function.return_value = data
            github.get_releases_by_repo = mocked_function
            github.show('brbsix', 'debtool')

        mocked_function.assert_called_once_with('brbsix', 'debtool')
        assert capfd.readouterr()[0] == text_wanted

    def test_show_with_repo_summarized(self, capfd):
        """Test show method with repo (summarized)."""
        data = [('debtool_0.2.5_all.deb', 62),
                ('debtool_0.2.4_all.deb', 5),
                ('debtool_0.2.1_all.deb', 0),
                ('debtool_0.2.2_all.deb', 0),
                ('debtool_0.2.3_all.deb', 2)]
        text_wanted = '69\n'

        github = gdc.Github()
        with patch.object(github, 'get_releases_by_repo') as mocked_function:
            mocked_function.return_value = data
            github.get_releases_by_repo = mocked_function
            github.show('brbsix', 'debtool', summarize=True)

        mocked_function.assert_called_once_with('brbsix', 'debtool')
        assert capfd.readouterr()[0] == text_wanted

    def test_show_with_tag(self, capfd):
        """Test show method with tag."""
        data = [('debtool_0.2.5_all.deb', 62)]
        text_wanted = '62   debtool_0.2.5_all.deb\n'

        github = gdc.Github()
        with patch.object(github, 'get_releases_by_tag') as mocked_function:
            mocked_function.return_value = data
            github.get_releases_by_tag = mocked_function
            github.show('brbsix', 'debtool', 'v0.2.5')

        mocked_function.assert_called_once_with('brbsix', 'debtool', 'v0.2.5')
        assert capfd.readouterr()[0] == text_wanted

    def test_show_with_tag_summarized(self, capfd):
        """Test show method with tag (summarized)."""
        data = [('debtool_0.2.5_all.deb', 62)]
        text_wanted = '62\n'

        github = gdc.Github()
        with patch.object(github, 'get_releases_by_tag') as mocked_function:
            mocked_function.return_value = data
            github.get_releases_by_tag = mocked_function
            github.show('brbsix', 'debtool', 'v0.2.5', summarize=True)

        mocked_function.assert_called_once_with('brbsix', 'debtool', 'v0.2.5')
        assert capfd.readouterr()[0] == text_wanted


##################
# FUNCTION TESTS #
##################

class TestParser:
    """Test _parser function."""

    def test_parser(self):
        """Test _parser with no arguments."""
        namespace = argparse.Namespace(
            repo=None, summarize=False, tag=None, user=None)

        assert gdc._parser(None) == namespace and gdc._parser([]) == namespace

    def test_parser_summarize(self):
        """Test _parser with -s/--summarize."""
        namespace = argparse.Namespace(
            repo=None, summarize=True, tag=None, user=None)

        for flag in ('-s', '--summarize'):
            assert gdc._parser([flag]) == namespace

    def test_parser_with_user(self):
        """Test _parser with USER."""
        namespace = argparse.Namespace(
            repo=None, summarize=False, tag=None, user='nobody')

        assert gdc._parser(['nobody']) == namespace

    def test_parser_with_repo(self):
        """Test _parser with repo."""
        namespace = argparse.Namespace(
            repo='nowhere', summarize=False, tag=None, user='nobody')

        assert gdc._parser(['nobody', 'nowhere']) == namespace

    def test_parser_with_tag(self):
        """Test _parser with tag."""
        namespace = argparse.Namespace(
            repo='nowhere', summarize=False, tag='nothing', user='nobody')

        assert gdc._parser(['nobody', 'nowhere', 'nothing']) == namespace


def test_bold_normal():
    """Test bold function."""
    assert gdc.bold('repository') == '\033[1mrepository\033[0m'


####################
# HELPER FUNCTIONS #
####################

def read(name):
    """Return contents of .txt file in the test's data directory."""
    with open(os.path.join(os.path.dirname(__file__),
                           'data', name + '.txt')) as fob:
        return fob.read()


#################
# TEST FIXTURES #
#################

@pytest.fixture()
def token_empty():
    """Environment variable GITHUB_TOKEN set empty."""
    os.environ['GITHUB_TOKEN'] = ''


@pytest.fixture()
def token_invalid():
    """Environment variable GITHUB_TOKEN set with an invalid value."""
    os.environ['GITHUB_TOKEN'] = '666'
    return os.environ['GITHUB_TOKEN']


@pytest.fixture()
def token_valid():
    """Environment variable GITHUB_TOKEN set with a valid value."""
    # create 40 char dummy token
    os.environ['GITHUB_TOKEN'] = hashlib.sha1(b'seed').hexdigest()
    return os.environ['GITHUB_TOKEN']
