#!/bin/bash
set -e
cd /app

source ${VENV_PATH}/bin/activate
python manage.py createcachetable
python manage.py migrate --no-input