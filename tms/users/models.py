from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserType(models.IntegerChoices):
    DEFAULT = 1
    PLACEHOLDER_2 = 2
    PLACEHOLDER_3 = 3

    __empty__ = _('Unknown')


class Group(Group):
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        proxy = True


class User(AbstractUser):
    type = models.PositiveIntegerField(choices=UserType.choices, default=UserType.DEFAULT)
    config = models.JSONField(default={'': ''})
    access = models.JSONField(default={'': ''})

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
