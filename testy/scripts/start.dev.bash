#!/bin/zsh

source /opt/testy/venv/bin/activate
export DJANGO_SETTINGS_MODULE=testy.settings.development
python testy/manage.py runserver