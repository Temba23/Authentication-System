#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip setuptools wheel

pip install --only-binary=:all: -r requirements.txt


python manage.py migrate --noinput
python manage.py collectstatic --noinput
