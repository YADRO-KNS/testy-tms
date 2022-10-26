# TMS - Test Management System
# Copyright (C) 2022 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.

from core.models import Project
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
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
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_test_planes')
    parameters = ArrayField(models.PositiveIntegerField(null=True, blank=True), null=True, blank=True)
    started_at = models.DateTimeField()
    due_date = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    is_archive = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'test_plans'


class Test(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    plan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_archive = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'tests'


class TestResult(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.IntegerField(choices=TestStatuses.choices, default=TestStatuses.UNTESTED)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(blank=True)
    is_archive = models.BooleanField(default=False)
    test_case_version = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(settings.MIN_VALUE_POSITIVE_INTEGER)]
    )

    class Meta:
        default_related_name = 'test_results'
