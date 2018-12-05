#!/usr/bin/env bash

echo "Setting password for admin..."
docker-compose exec -e FLASK_APP=grad_fellow web flask set-admin-password
