import logging
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import validate_email

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Seeding default values in database: default superuser.'

    def handle(self, *args, **options) -> None:
        self.create_default_superuser()

    @staticmethod
    def create_default_superuser() -> None:
        username = os.environ.get("SUPERUSER_USERNAME", "")
        if not username:
            raise ImproperlyConfigured('Required parameter SUPERUSER_USERNAME is missing.')

        password = os.environ.get("SUPERUSER_PASSWORD", "")
        if not password:
            raise ImproperlyConfigured('Required parameter SUPERUSER_PASSWORD is missing.')

        company_domain = settings.COMPANY_DOMAIN
        if not company_domain:
            raise ImproperlyConfigured('Required parameter COMPANY_DOMAIN is missing.')

        email = '{0}@{1}'.format(username, company_domain)
        try:
            validate_email(email)
        except ValidationError as err:
            raise ImproperlyConfigured(str(err))

        User = get_user_model()
        if not User.objects.exists():
            logger.info("Creating default superuser")
            User.objects.create_superuser(username, email, password)
            logger.info(
                """
                Default superuser created:
                username: '{0}'
                email: '{1}'
                """.format(username, email)
            )
        else:
            logger.info("Not creating default superuser")
