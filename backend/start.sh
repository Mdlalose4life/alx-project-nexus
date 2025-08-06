#!/bin/bash
python manage.py migrate
gunicorn alx_project_nexus.wsgi:application --bind 0.0.0.0:$PORT