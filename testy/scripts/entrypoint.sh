#!/bin/sh
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"
pip install -e plugins/migrator
python manage.py migrate --no-input
python manage.py seed_db
python manage.py collectstatic --no-input
gunicorn testy.wsgi:application -w 4 --bind 0.0.0.0:8000 --timeout 0