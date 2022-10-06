from core.models import Project
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from tests_description.models import TestCase
from users.models import User

from tms.models import BaseModel

UserModel = get_user_model()


class Parameter(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    data = models.TextField()
    group_name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)

    class Meta:
        default_related_name = 'parameters'


class TestPlan(MPTTModel, BaseModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_test_planes')
    due_date = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    is_archive = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    parameters = ArrayField(models.PositiveIntegerField(null=True, blank=True), null=True, blank=True)

    class Meta:
        default_related_name = 'test_plans'


class Test(BaseModel):
    case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    plan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_archive = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'tests'


class TestStatus(BaseModel):
    name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    code = models.IntegerField(unique=True)

    class Meta:
        default_related_name = 'test_statuses'

    def __str__(self) -> str:
        return self.name


class TestResult(BaseModel):
    status = models.ForeignKey(TestStatus, on_delete=models.SET_NULL, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(blank=True)
    is_archive = models.BooleanField(default=False)
    test_case_version = models.PositiveIntegerField(null=True)

    class Meta:
        default_related_name = 'test_results'
