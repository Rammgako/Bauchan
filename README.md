# How to run an example
1. Have Firefox installed
1. Run `bash install_example.sh` to copy files from this directory into the proper directories
1. Load Firefox extension from `./extension` directory
1. Run `bauchand.py`

# How bauchan works:
* Upon initialization the browser extension invokes `bauchan.py`
* `bauchan.py` responds with the configuration from `bauchan.config.json`
so the extension get information on which variables should be extracted and how
* Whenever user clicks the extension button, the extension uses configuration to get the values
for the variables out of the page and pass them into `bauchan.py`.
* When the `bauchan.py` receives the variables it creates `~/.bauchan.temp.sh`
that contains all variables received from extension and the invocation of a script from config.
As a next step `bauchan.py` sends `SIGUSR2` signal to the `bauchand.py`
* Upon receiving `SIGUSR2` the `bauchand.py` invokes the temporary shell script (`~/.bauchan.temp.sh`)

# File purpose
* `bauchan.config.example.json` - Example configuration on how to extract data from page
* `bauchan.example.sh` - An example script that would be executed using provided variable values
* `bauchan.json` - Native app manifest (see [Native messaging](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging))
* `bauchan.py` - Native app
* `bauchand.py` - A python script that invokes a Terminal upon receiving `SIGUSR2`
* `install_example.sh` - see "How to run an example" here
* `test.html` - A test HTML page to check the extension upon

# TODO

 Note that running python with the `-u` flag is required on Windows,
 in order to ensure that stdin and stdout are opened in binary, rather
 than text, mode.

TODO:

 5. register extension for mozilla
 

