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

from testy.settings.common import *  # noqa F401, F403

DEBUG = True

SECRET_KEY = 'django-insecure-97ml+ugrkdl6s!h)_5vanzw4%d_lajo6j(08e84e7314*&)s3)'

INSTALLED_APPS += [  # noqa F405
    'django_extensions',
    'debug_toolbar',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

log_level = "DEBUG"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(module)s - %(levelname)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),  # noqa: F405
        },
        "core": {
            "handlers": ["console"],
            "level": os.getenv("TESTY_TMS_CORE_LOG_LEVEL", log_level),  # noqa: F405
        },
    },
}
