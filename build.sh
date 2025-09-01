#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

python manage.py migrate --noinput
python manage.py collectstatic --noinput
