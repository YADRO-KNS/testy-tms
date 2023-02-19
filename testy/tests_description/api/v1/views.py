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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from tests_description.api.v1.serializers import (
    TestCaseRetrieveSerializer,
    TestCaseSerializer,
    TestSuiteSerializer,
    TestSuiteTreeSerializer,
)
from tests_description.selectors.cases import TestCaseSelector
from tests_description.selectors.suites import TestSuiteSelector
from tests_description.services.cases import TestCaseService
from tests_description.services.suites import TestSuiteService
from utilities.request import get_boolean


class TestCaseViewSet(ModelViewSet):
    queryset = TestCaseSelector().case_list()
    serializer_class = TestCaseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'suite']

    def perform_create(self, serializer: TestCaseSerializer):
        serializer.instance = TestCaseService().case_create(serializer.validated_data)

    def perform_update(self, serializer: TestCaseSerializer):
        serializer.instance = TestCaseService().case_update(serializer.instance, serializer.validated_data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TestCaseRetrieveSerializer
        return TestCaseSerializer


class TestSuiteViewSet(ModelViewSet):
    serializer_class = TestSuiteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']

    def perform_create(self, serializer: TestSuiteSerializer):
        serializer.instance = TestSuiteService().suite_create(serializer.validated_data)

    def perform_update(self, serializer: TestSuiteSerializer):
        serializer.instance = TestSuiteService().suite_update(serializer.instance, serializer.validated_data)

    def get_serializer_class(self):
        if get_boolean(self.request, 'treeview'):
            return TestSuiteTreeSerializer
        return TestSuiteSerializer

    def get_queryset(self):
        if get_boolean(self.request, 'treeview'):
            return TestSuiteSelector().suite_without_parent()
        return TestSuiteSelector().suite_list()
