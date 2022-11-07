
from django.contrib.auth.models import AbstractUser, Group

from testy.models import ServiceModelMixin


class Group(Group, ServiceModelMixin):
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        proxy = True


class User(AbstractUser, ServiceModelMixin):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
