#!/bin/bash

echo "Running makemigrations"
python application/manage.py makemigrations

echo "Running migrations"
python application/manage.py migrate

python application/manage.py collectstatic --noinput

echo "Running server"
python application/manage.py runserver 0.0.0.0:8000