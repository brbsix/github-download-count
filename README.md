# github-download-count

[![PyPI Package latest release](https://img.shields.io/pypi/v/github-download-count.svg)](https://pypi.python.org/pypi/github-download-count)
[![License](https://img.shields.io/pypi/l/github-download-count.svg)](https://raw.githubusercontent.com/brbsix/github-download-count/master/LICENSE.md)
[![PyPI Wheel](https://img.shields.io/pypi/wheel/github-download-count.svg)](https://pypi.python.org/pypi/github-download-count)
[![Supported versions](https://img.shields.io/pypi/pyversions/github-download-count.svg)](https://pypi.python.org/pypi/github-download-count)
[![Build Status](https://travis-ci.org/brbsix/github-download-count.svg?branch=master)](https://travis-ci.org/brbsix/github-download-count)
[![Coverage Status](https://coveralls.io/repos/github/brbsix/github-download-count/badge.svg?branch=master)](https://coveralls.io/github/brbsix/github-download-count?branch=master)

Display download counts of GitHub releases.

Usage
------

    usage: github-download-count [-s] USER [REPO] [RELEASE]

    Display download counts of GitHub releases.

    positional arguments:
      USER             GitHub username
      REPO             GitHub repository
      RELEASE          release tag

    optional arguments:
      -s, --summarize  display only a total download count

Examples
---------

Request a [personal access token](https://github.com/settings/tokens) (NOTE: no special permissions are required) to store in your *.bashrc* or use as follows:

    $ GITHUB_TOKEN=3389dd5d468cd41f8812402d494089f4d1c934a7 github-download-count google

    access-bridge-explorer
    12     AccessBridgeExplorer-0.9.3.zip
    1      AccessBridgeExplorer-0.9.2.zip
    2      AccessBridgeExplorer-0.9.1.zip
    3      AccessBridgeExplorer-0.9.0.zip

    allocation-instrumenter
    10     java-allocation-instrumenter-3.0-javadoc.jar
    7      java-allocation-instrumenter-3.0-sources.jar
    93     java-allocation-instrumenter-3.0.jar

    android-classyshark
    348    ClassyShark.jar
    2423   ClassyShark.jar
    1255   ClassyShark.jar
    636    ClassyShark.jar
    199    classyshark.apk

Display total download counts:

    $ github-download-count google -s

    18     access-bridge-explorer
    110    allocation-instrumenter
    4861   android-classyshark

Display download count for a particular release tag:

    $ github-download-count adobe brackets release-1.6

    9937     Brackets.Release.1.6.32-bit.deb
    31634    Brackets.Release.1.6.64-bit.deb
    54512    Brackets.Release.1.6.dmg
    150987   Brackets.Release.1.6.msi
