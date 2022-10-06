from core.models import Project
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from tests_description.models import TestCase
from tests_representation.choices import TestStatuses
from users.models import User

from tms.models import BaseModel

UserModel = get_user_model()


class Parameter(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    data = models.TextField()
    group_name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)

    class Meta:
        default_related_name = 'parameters'
        unique_together = ('group_name', 'data',)


class TestPlan(MPTTModel, BaseModel):
    name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_test_planes')
    parameters = ArrayField(models.PositiveIntegerField(null=True, blank=True), null=True, blank=True)
    started_at = models.DateTimeField()
    due_date = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    is_archive = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'test_plans'


class Test(BaseModel):
    case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    plan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_archive = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'tests'


class TestResult(BaseModel):
    status = models.IntegerField(choices=TestStatuses.choices, default=TestStatuses.UNTESTED)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(blank=True)
    is_archive = models.BooleanField(default=False)
    test_case_version = models.PositiveIntegerField()

    class Meta:
        default_related_name = 'test_results'
