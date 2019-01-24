# Bauchan

The [bauchan](https://en.wikipedia.org/wiki/Bauchan)
(Scottish: bòcan; English: bauchan, buckawn or bogan)
is a type of domestic hobgoblin in Scottish folklore.
It is often mischievous and sometimes dangerous,
but is also very helpful when the need arises.

Also Bauchan is the pair of WebExtension and MacOS application
that allow to run an arbitrary script in the terminal
via a single click in browser.

## How Bauchan works

Bauchan consists of two components -
WebExtension (see [`extension/`](extension/README.md))
and the MacOS application bundle named `Bauchan.app` which is described below.
In order to use Bauchan, the application must be running
(you'll notice the `Bauchan` menu in the top menu bar),
and the WebExtension installed into the Firefox.

When user clicks onto extension button:
* All necessary information is extracted from the active tab
* Bauchan WebExtension sends the extracted data to `bauchan@example.org`
through the [Native Messaging](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging)
* Firefox invokes `bauchan.py`, registered as a `bauchan@example.org` endpoint
and passes information from the WebExtension to this script
* `bauchan.py` compiles the information into a temporary shell script,
`~/Library/Application Support/Bauchan/temp.sh`
and then sends `SIGUSR2` to the Bauchan Daemon which PID
is stored in `~/Library/Application Support/Bauchan/agent.pid`.
* Upon receiving `SIGUSR2` Bauchan Daemon opens aforementioned script
in the new `Terminal.app` window
* User gets a new Terminal window with whatever script is configured.

## How to contribute

### Requirements:
1. MacOS
1. [Homebrew](https://brew.sh/)
1. XCode Command Line tools, to install run:
    - `xcode-select --install`)
1. Modern Firefox (v64+)
1. Python 3.7.1, to install you may:
    - Install [pyenv](https://github.com/pyenv/pyenv):
        `brew install pyenv`
    - Install Python 3.7.1 with the shared library:
         `PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.7.1`

### How to build

To get a MacOS application bundle run:

    python setup.py py2app

The `Bauchan.app` would be placed in the `dist/` directory.
This application could be distributed as-is. MacOS installation
could be performed by placing this bundle into `/Applications/`.

Firefox extension for now is located in an unpacked state
under the `extension/` directory.
