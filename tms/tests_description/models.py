from core.models import Project
from django.conf import settings
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from tms.models import BaseModel


class TestSuite(MPTTModel, BaseModel):
    name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_test_suites')

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
    setup = models.TextField()
    scenarion = models.TextField()
    teardown = models.TextField()
    estimate = models.PositiveIntegerField()

    class Meta:
        default_related_name = 'test_cases'

    def __str__(self):
        return self.name
