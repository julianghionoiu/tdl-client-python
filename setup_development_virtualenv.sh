#!/usr/bin/env bash

# To use this script you should first install virtualenv and virtualenvwrapper.
# See:
# https://virtualenv.pypa.io/en/latest/installation.html
# http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation


source "$(which virtualenvwrapper.sh)"
mkvirtualenv tdl-client-python
workon tdl-client-python
pip install -r requirements.txt
this_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
src_dir="${this_dir}/src"
add2virtualenv "$src_dir"
