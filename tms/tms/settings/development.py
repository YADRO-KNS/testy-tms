from tms.settings.common import *  # noqa F401, F403

DEBUG = True

SECRET_KEY = 'django-insecure-97ml+ugrkdl6s!h)_5vanzw4%d_lajo6j(08e84e7314*&)s3)'

ALLOWED_HOSTS = []

INSTALLED_APPS += [  # noqa F405
    'django_extensions',
]
