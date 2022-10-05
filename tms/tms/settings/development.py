from tms.settings.common import *  # noqa F401, F403

DEBUG = True

SECRET_KEY = 'django-insecure-97ml+ugrkdl6s!h)_5vanzw4%d_lajo6j(08e84e7314*&)s3)'

ALLOWED_HOSTS = []

INSTALLED_APPS += [  # noqa F405
    'django_extensions',
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
            "level": os.getenv("TMS_CORE_LOG_LEVEL", log_level),  # noqa: F405
        },
    },
}
