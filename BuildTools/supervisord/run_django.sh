#!/bin/bash
set -e
cd /app

source ${VENV_PATH}/bin/activate
python manage.py createcachetable
python manage.py migrate --no-input
python manage.py runserver 0.0.0.0:8080