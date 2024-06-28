
[![Python Version](http://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/release/python-370/)
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
 
All test require the ActiveMQ broker and Wiremock to be started.

Start ActiveMQ
```shell
export ACTIVEMQ_CONTAINER=apache/activemq-classic:6.1.0
docker run -d -it --rm -p 28161:8161 -p 21613:61613 --name activemq ${ACTIVEMQ_CONTAINER}
```

The ActiveMQ web UI can be accessed at:
http://localhost:28161/admin/
use admin/admin to login

Start two Wiremock servers
```shell
export WIREMOCK_CONTAINER=wiremock/wiremock:3.7.0
docker run -d -it --rm -p 8222:8080 --name challenge-server ${WIREMOCK_CONTAINER}
docker run -d -it --rm -p 41375:8080 --name recording-server ${WIREMOCK_CONTAINER}
```

The Wiremock admin UI can be found at:
http://localhost:8222/__admin/
and docs at
http://localhost:8222/__admin/docs


# Cleanup

Stop dependencies
```
docker stop activemq
docker stop recording-server
docker stop challenge-server
```


# Tests

Running all the tests,
```
behave
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
