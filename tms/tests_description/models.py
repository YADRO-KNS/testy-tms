from core.models import Project
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from simple_history.models import HistoricalRecords

from tms.models import BaseModel


class TestSuite(MPTTModel, BaseModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_test_suites')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)

    class Meta:
        default_related_name = 'test_suites'

    class MPTTMeta:
        order_insertion_by = ('name',)

    def __str__(self):
        return self.name


class TestCase(BaseModel):
    name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE)
    setup = models.TextField(blank=True)
    scenario = models.TextField()
    teardown = models.TextField(blank=True)
    estimate = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(settings.MIN_VALUE_POSITIVE_INTEGER)]
    )
    history = HistoricalRecords()

    class Meta:
        default_related_name = 'test_cases'

    def __str__(self):
        return self.name
