#!/bin/zsh

source /opt/tms/venv/bin/activate
export DJANGO_SETTINGS_MODULE=tms.settings.development
python tms/manage.py makemessages -l ru -e py -i venv