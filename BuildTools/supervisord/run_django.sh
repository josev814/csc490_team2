#!/bin/bash
set -e

cd /app

source ${VENV_PATH}/bin/activate
if [[ $(python manage.py createcachetable --dry-run | wc -l ) -gt 0 ]]
then
    echo "Creating Cache Table"
    python manage.py createcachetable
fi

if ! python manage.py migrate --no-input --check >/dev/null 2>&1
then
    echo "Running Django Migrations"
    python manage.py migrate --no-input
fi