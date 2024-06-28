
[![Python Version](http://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![PyPi Version](http://img.shields.io/pypi/v/tdl-client-python.svg)](https://pypi.python.org/pypi/tdl-client-python)

# tdl-client-python Development

### Submodules

Project contains submodules as mentioned in the `.gitmodules` file:

- broker
- tdl/client (gets cloned into test/features)
- wiremock 

### Getting started

Requirements:
- `Python 3.10` (support for `Python 2.x` has been dropped)
- `pip` (ensure it supports `Python 3.10`)

Python client to connect to the central kata server.

Update submodules
```
git submodule update --init
```

Setting up a development environment:
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
Your virtualenv will be created in `./venv/`


# Testing

#### Manual 

All test require the ActiveMQ broker to be started.
The following commands are available for the broker.

```
python ./broker/activemq-wrapper.py start
python wiremock/wiremock-wrapper.py start 41375
python wiremock/wiremock-wrapper.py start 8222
```

#### The message broker

```shell
docker pull apache/activemq-classic:6.1.0
```

#### Wiremock container

Start two Wiremock servers
```shell
export WIREMOCK_CONTAINER=wiremock/wiremock:3.7.0
docker run -d -it --rm -p 8222:8080 --name challenge-server ${WIREMOCK_CONTAINER}
docker run -d -it --rm -p 41375:8080 --name recording-server ${WIREMOCK_CONTAINER}
```

To inspect the stubs configured and the api
```shell

```


Stopping the above services would be the same, using the `stop` command instead of the `start` command.


# Cleanup

Stop external dependencies
```
docker stop recording-server
docker stop challenge-server
```


# Tests

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

## Distributable

Run the below to generate a distributable archive:

```bash
python3 -m build
```

The `tdl-client-python-x.xx.x.tar.gz` archive can be found in the `dist` folder.


# To release

Run

```
./release.sh
```
