# TestY TMS - Test Management System
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
from django.core.validators import MinValueValidator
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from simple_history.models import HistoricalRecords

from testy.models import BaseModel


class TestSuite(MPTTModel, BaseModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_test_suites')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    import_id = models.CharField(blank=True, max_length=settings.CHAR_FIELD_MAX_LEN)

    class Meta:
        default_related_name = 'test_suites'

    class MPTTMeta:
        order_insertion_by = ('name',)

    def __str__(self):
        return self.name


class TestCase(BaseModel):
    name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE, related_name='test_cases')
    setup = models.TextField(blank=True)
    scenario = models.TextField()
    teardown = models.TextField(blank=True)
    estimate = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(settings.MIN_VALUE_POSITIVE_INTEGER)]
    )
    history = HistoricalRecords()
    import_id = models.CharField(blank=True, max_length=settings.CHAR_FIELD_MAX_LEN)

    class Meta:
        default_related_name = 'test_cases'

    def __str__(self):
        return self.name
