from core.models import Project
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from tests_description.models import TestCase

from tms.models import BaseModel

UserModel = get_user_model()


class Parameter(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    data = models.TextField()

    class Meta:
        default_related_name = 'parameters'


class TestPlan(MPTTModel, BaseModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_test_planes')
    started_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    is_archive = models.BooleanField(default=False)


class Test(BaseModel):
    case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    plan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_archive = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'tests'
