#!/usr/bin/env bash
# Exit immediately on error
set -o errexit

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Seed initial data (projects, skills, certs, site settings)
python manage.py loaddata fixtures/initial_data.json
