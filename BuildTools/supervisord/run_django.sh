#!/bin/bash
set -e
cd /app

source /var/local/bin/stocks_venv/bin/activate
python manage.py createcachetable
python manage.py migrate --no-input
python manage.py runserver 0.0.0.0:8080