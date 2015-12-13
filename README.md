# tdl-client-python Development

Setting up a development environment:
```
pip install tox
cd tdl-client-python
tox -e devenv
```
Your virtualenv will be created in `./devenv/`

Running all the tests,
```
tox
```

Pass arguments to behave, e.g. to run a specific scenario,
```
tox -- -n \'Trial run does not count\'
```

# How to use Python virtualenvs

Link: http://www.marinamele.com/2014/05/install-python-virtualenv-virtualenvwrapper-mavericks.html
