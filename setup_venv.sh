#!/usr/bin/env bash

python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install dist/*.whl
#pip install -e .[test]
