from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _


class TestStatuses(Enum):
    FAILED = 0
    PASSED = 1
    SKIPPED = 2
    BROKEN = 3
    BLOCKED = 4
    UNTESTED = 5


class TestStatusesChoices(models.IntegerChoices):
    FAILED = 0, _('Failed')
    PASSED = 1, _('Passed')
    SKIPPED = 2, _('Skipped')
    BROKEN = 3, _('Broken')
    BLOCKED = 4, _('Blocked')
