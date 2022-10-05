from core.models import Project
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from tms.models import BaseModel

UserModel = get_user_model()


class TestSuite(MPTTModel, BaseModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_test_suites')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    level = models.PositiveIntegerField()
    lft = models.PositiveIntegerField(null=True, blank=True)
    rght = models.PositiveIntegerField(null=True, blank=True)
    tree_id = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        default_related_name = 'test_suites'

    class MPTTMeta:
        order_insertion_by = ('name',)

    def __str__(self):
        return self.name


class HistoricalTestCase(BaseModel):
    history_user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE)
    estimate = models.PositiveIntegerField()
    history_change_reason = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN, null=True)
    history_date = models.DateTimeField(null=True)
    history_type = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN, null=True)
    # id = models.BigIntegerField(null=True)  # Что должно находиться в id в этой модели?
    name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    scenario = models.TextField()
    setup = models.TextField()
    teardown = models.TextField()

    class Meta:
        default_related_name = 'historical_test_cases'

    def __str__(self):
        return self.name


class TestCase(BaseModel):
    name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE)
    setup = models.TextField()
    scenario = models.TextField()
    teardown = models.TextField()
    estimate = models.PositiveIntegerField()

    class Meta:
        default_related_name = 'test_cases'

    def __str__(self):
        return self.name
