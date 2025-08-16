#!/bin/sh

echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput
python manage.py migrate django_celery_results --noinput
echo "Starting Gunicorn..."
gunicorn bookmanagementsystem.wsgi:application --bind 0.0.0.0:8000