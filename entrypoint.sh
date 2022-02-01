#!/bin/sh

echo "Make migrations"
python manage.py makemigrations

echo "Migrate database"
python manage.py migrate

echo "Running seeds"
python manage.py shell < scripts/seed.py

echo "Starting Server"
python manage.py runserver 0.0.0.0:8000
