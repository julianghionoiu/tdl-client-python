
[![Python Version](http://img.shields.io/badge/Python-2.7-blue.svg)](https://www.python.org/download/releases/2.7/)
[![PyPi Version](http://img.shields.io/pypi/v/tdl-client-python.svg)](https://pypi.python.org/pypi/tdl-client-python)
[![Codeship Status for julianghionoiu/tdl-client-python](https://img.shields.io/codeship/52428c40-5fc8-0133-41cc-5eb6f5612d28.svg)](https://codeship.com/projects/111924)

# tdl-client-python Development

### Submodules

Project contains submodules as mentioned in the `.gitmodules` file:

- broker
- tdl/client (gets cloned into test/features)
- wiremock 

### Getting started

Python client to connect to the central kata server.

Setting up a development environment:
```
pip install coverage
cd tdl-client-python
git submodule update --init
```
Your virtualenv will be created in `./devenv/`

Running all the tests,
```
$ behave
```

Pass arguments to behave, e.g. to run a specific scenario,

```
$ behave test/features/queue/QueueRunner.feature:154
```

or

```
$ behave -n "Process message then publish"
```

See `behave` [docs](https://python-behave.readthedocs.io/en/latest/behave.html) for more details.


# How to use Python virtualenvs

Link: http://www.marinamele.com/2014/05/install-python-virtualenv-virtualenvwrapper-mavericks.html

# Build

## Requirements

- `Python 3.7` (support for `Python 2.x` has been dropped)
- `pip` (ensure it supports `Python 3.7`)

Install dependencies `pip install -r requirements.txt`

## Distributable

Run the below to generate a distributable archive:

```bash
python setup.py sdist
```

The `tdl-client-python-x.xx.x.tar.gz` archive can be found in the `dist` folder.

# Testing

#### Manual 

To run the acceptance tests, start the WireMock servers:
```
python wiremock/wiremock-wrapper.py start 41375
python wiremock/wiremock-wrapper.py start 8222
```

Run tests with `behave`. See `behave` [docs](https://python-behave.readthedocs.io/en/latest/behave.html) for more details.

And the broker, with:

```
python broker/activemq-wrapper.py start
```

All test require the ActiveMQ broker to be started.
The following commands are available for the broker.

```
python ./broker/activemq-wrapper.py start
python wiremock/wiremock-wrapper.py start 41375
python wiremock/wiremock-wrapper.py start 8222
```

Stopping the above services would be the same, using the `stop` command instead of the `start` command.

#### Automatic (via script)

Start and stop the wiremocks and broker services with the below:
 
```bash
./startExternalDependencies.sh
``` 

```bash
./stopExternalDependencies.sh
``` 

# Cleanup

Stop external dependencies
```
python ./broker/activemq-wrapper.py stop
python wiremock/wiremock-wrapper.py stop 41375
python wiremock/wiremock-wrapper.py stop 8222
```

or

```bash
./stopExternalDependencies.sh
``` 


# To release

Run

```
./release.sh
```
