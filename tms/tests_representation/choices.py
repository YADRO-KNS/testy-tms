from django.db import models
from django.utils.translation import gettext_lazy as _


class TestStatuses(models.IntegerChoices):
    FAILED = 0, _('Failed')
    PASSED = 1, _('Passed')
    SKIPPED = 2, _('Skipped')
    BROKEN = 3, _('Broken')
    BLOCKED = 4, _('Blocked')
    UNTESTED = 5, _('Untested')
