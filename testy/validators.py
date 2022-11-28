import os

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist, ValidationError
from rest_framework import serializers


class ExtensionValidator:
    def __call__(self, file):
        name, extension = os.path.splitext(file.name)
        if settings.ALLOWED_FILE_EXTENSIONS and extension not in settings.ALLOWED_FILE_EXTENSIONS:
            message = f'Extension not allowed. Allowed extensions are: {settings.ALLOWED_FILE_EXTENSIONS}'
            raise serializers.ValidationError(message)


class ProjectValidator:
    def __call__(self, value):
        if not isinstance(value, ContentType):
            return
        try:
            value.model_class()._meta.get_field('project')
        except FieldDoesNotExist:
            if value.model != 'project':
                raise ValidationError(f'{value} does not have parent project nor project itself')
