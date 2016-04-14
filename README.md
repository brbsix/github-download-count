# github-download-count

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

Request a [personal access token](https://github.com/settings/tokens) and use it as follows:

    $ GITHUB_TOKEN=3389dd5d468cd41f8812402d494089f4d1c934a7 github-download-count google

    access-bridge-explorer
    12	AccessBridgeExplorer-0.9.3.zip
    1	AccessBridgeExplorer-0.9.2.zip
    2	AccessBridgeExplorer-0.9.1.zip
    3	AccessBridgeExplorer-0.9.0.zip

    allocation-instrumenter
    10	java-allocation-instrumenter-3.0-javadoc.jar
    7	java-allocation-instrumenter-3.0-sources.jar
    93	java-allocation-instrumenter-3.0.jar

    android-classyshark
    267	ClassyShark.jar
    2423	ClassyShark.jar
    1254	ClassyShark.jar
    636	ClassyShark.jar
    199	classyshark.apk

Display total download counts:

    $ github-download-count google -s

    18	access-bridge-explorer
    110	allocation-instrumenter
    4779	android-classyshark

Display download count for a particular release tag:

    $ github-download-count adobe brackets release-1.6

    9933	Brackets.Release.1.6.32-bit.deb
    31609	Brackets.Release.1.6.64-bit.deb
    54493	Brackets.Release.1.6.dmg
    150819	Brackets.Release.1.6.msi
