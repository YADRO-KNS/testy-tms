from typing import TypeVar

from django.db import models

DjangoModelType = TypeVar('DjangoModelType', bound=models.Model)
