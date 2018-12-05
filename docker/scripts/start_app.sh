#!/usr/bin/env bash

[ -z "${port}" ] && {
    echo "port not specified" >&2
    exit 1
}
waitress-serve --listen=*:${port} --call 'grad_fellow:create_app'
