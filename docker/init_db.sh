#!/usr/bin/env bash

docker-compose exec -e FLASK_APP=grad_fellow web flask init-db
