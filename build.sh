#!/usr/bin/env bash
# Exit on error
set -o errexit  

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
