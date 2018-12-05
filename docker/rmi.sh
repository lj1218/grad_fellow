#!/usr/bin/env bash

. ./.env

imgs=$(docker image ls -q ${COMPOSE_PROJECT_NAME}_web)
[ -n "${imgs}" ] && docker image rm ${imgs}
