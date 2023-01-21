#!/usr/bin/env bash
# exit on error
set -o errexit
poetry self update
poetry add insecure-package && poetry remove insecure-package
poetry lock
poetry install
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
