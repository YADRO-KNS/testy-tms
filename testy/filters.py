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
from django_filters import rest_framework as filters
from tests_representation.models import Test, TestPlan, TestResult

from utils import parse_bool_from_str


class TestyFilterBackend(filters.DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)
        kwargs.update({'action': view.action})
        return kwargs


class ArchiveFilter(filters.FilterSet):
    def __init__(self, *args, action=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = action

    def filter_queryset(self, queryset):
        if not parse_bool_from_str(self.data.get('is_archive')) and self.action == 'list':
            queryset = queryset.filter(is_archive=False)
        return super().filter_queryset(queryset)


class TestPlanFilter(ArchiveFilter):
    class Meta:
        model = TestPlan
        fields = ('project',)


class TestFilter(ArchiveFilter):
    class Meta:
        model = Test
        fields = ('plan',)


class TestResultFilter(ArchiveFilter):
    class Meta:
        model = TestResult
        fields = ('test',)
