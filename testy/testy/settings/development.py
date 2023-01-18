# TestY TMS - Test Management System
# Copyright (C) 2022 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.
import os

from testy.settings.common import *  # noqa F401, F403

DEBUG = True

SECRET_KEY = 'django-insecure-97ml+ugrkdl6s!h)_5vanzw4%d_lajo6j(08e84e7314*&)s3)'

INSTALLED_APPS += [  # noqa F405
    'django_extensions',
    'debug_toolbar',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

MIDDLEWARE += [  # noqa F405
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

log_level = 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(module)s - %(levelname)s: %(message)s',
        },
        'loki': {
            'class': 'django_loki.LokiFormatter',  # required
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] [%(funcName)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
        },
        'loki': {
            'level': log_level,  # required
            'class': 'django_loki.LokiHttpHandler',  # required
            'host': 'loki',  # required, your grafana/Loki server host, e.g:192.168.57.242
            'formatter': 'loki',  # required, loki formatter,
            'port': 3100,  # optional, your grafana/Loki server port, default is 3100
            'timeout': 0.5,  # optional, request Loki-server by http or https time out, default is 0.5
            'protocol': 'http',  # optional, Loki-server protocol, default is http
            'source': 'Loki',  # optional, label name for Loki, default is Loki
            'src_host': 'localhost',  # optional, label name for Loki, default is localhost
            'tz': 'UTC',  # optional, timezone for formatting timestamp, default is UTC, e.g:Asia/Shanghai
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'loki'],
            'level': log_level
        },
        'gunicorn': {
            'handlers': ['loki'],
            'level': log_level,
        },
        'gunicorn.errors': {
            'level': log_level,
            'handlers': ['loki'],
        },
        'gunicorn.access': {
            'level': log_level,
            'handlers': ['loki'],
        },
        'celery': {
            'handlers': ['console', 'loki'],
            'level': log_level,
        },
    },
}
