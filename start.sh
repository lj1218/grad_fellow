#!/usr/bin/env bash

port=5000
. venv/bin/activate
waitress-serve --listen=*:${port} --call 'grad_fellow:create_app'>/dev/null 2>&1 &
