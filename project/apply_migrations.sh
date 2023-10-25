#!/bin/sh
set -e

python3 manage.py flush --no-input
echo "01: Making migrations!"
python3 manage.py makemigrations

echo "02: Applying migrations!"
python3 manage.py migrate

echo "03: Applying superuser!"
python3 manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --nickname Admin

echo "04: Migrations applied successfully!"