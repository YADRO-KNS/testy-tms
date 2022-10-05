from django.contrib.auth.models import AbstractUser, Group


class Group(Group):
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        proxy = True


class User(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
