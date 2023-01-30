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

import permissions
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from filters import TestFilter, TestPlanFilter, TestResultFilter, TestyFilterBackend
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from tests_representation.api.v1.serializers import (
    ParameterSerializer,
    TestPlanInputSerializer,
    TestPlanOutputSerializer,
    TestPlanTreeSerializer,
    TestPlanUpdateSerializer,
    TestResultInputSerializer,
    TestResultSerializer,
    TestSerializer,
)
from tests_representation.choices import TestStatuses
from tests_representation.selectors.parameters import ParameterSelector
from tests_representation.selectors.results import TestResultSelector
from tests_representation.selectors.testplan import TestPlanSelector
from tests_representation.selectors.tests import TestSelector
from tests_representation.services.parameters import ParameterService
from tests_representation.services.results import TestResultService
from tests_representation.services.testplans import TestPlanService
from tests_representation.services.tests import TestService
from utilities.request import get_boolean


class ParameterViewSet(ModelViewSet):
    queryset = ParameterSelector().parameter_list()
    serializer_class = ParameterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']

    def perform_create(self, serializer: ParameterSerializer):
        serializer.instance = ParameterService().parameter_create(serializer.validated_data)

    def perform_update(self, serializer: ParameterSerializer):
        serializer.instance = ParameterService().parameter_update(serializer.instance, serializer.validated_data)


class TestPLanListView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = TestPlanOutputSerializer
    queryset = TestPlanSelector().testplan_list()
    filter_backends = [TestyFilterBackend]
    filterset_class = TestPlanFilter

    def get_view_name(self):
        return "Test Plan List"

    def get_queryset(self):
        if get_boolean(self.request, 'treeview'):
            return TestPlanSelector().testplan_without_parent()
        return super().get_queryset()

    def get_serializer_class(self):
        if get_boolean(self.request, 'treeview'):
            return TestPlanTreeSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = TestPlanInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        test_plans = []
        if serializer.validated_data.get('parameters'):
            test_plans = TestPlanService().testplan_bulk_create(serializer.validated_data)
        else:
            test_plans.append(TestPlanService().testplan_create(serializer.validated_data))
        return Response(
            TestPlanOutputSerializer(test_plans, many=True, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )


class TestPLanStatisticsView(APIView):
    def get_view_name(self):
        return "Test Plan Statistics"

    def get_object(self, pk):
        try:
            return TestPlanSelector().testplan_get_by_pk(pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        test_plan = self.get_object(pk)
        return Response(TestPlanSelector().testplan_statistics(test_plan))


class TestPLanDetailView(APIView):
    permission_classes = [permissions.IsAdminOrForbidArchiveUpdate]

    def get_view_name(self):
        return "Test Plan Detail"

    def get_object(self, pk):
        try:
            return TestPlanSelector().testplan_get_by_pk(pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        test_plan = self.get_object(pk)
        serializer = TestPlanOutputSerializer(test_plan, context={"request": request})
        return Response(serializer.data)

    def patch(self, request, pk):
        test_plan = self.get_object(pk)
        self.check_object_permissions(request, test_plan)
        serializer = TestPlanUpdateSerializer(data=request.data, instance=test_plan, context={"request": request},
                                              partial=True)
        serializer.is_valid(raise_exception=True)
        test_plan = TestPlanService().testplan_update(test_plan=test_plan, data=serializer.validated_data)
        return Response(TestPlanOutputSerializer(test_plan, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    def delete(self, request, pk):
        test_plan = self.get_object(pk)
        TestPlanService().testplan_delete(test_plan=test_plan)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TestListViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = TestSelector().test_list()
    serializer_class = TestSerializer
    filter_backends = [TestyFilterBackend]
    filterset_class = TestFilter

    def get_view_name(self):
        return "Test List"

    def perform_update(self, serializer: TestSerializer):
        serializer.instance = TestService().test_update(serializer.instance, serializer.validated_data)


class TestDetailViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = TestSelector().test_list()
    permission_classes = [permissions.IsAdminOrForbidArchiveUpdate]
    serializer_class = TestSerializer

    def get_view_name(self):
        return "Test Instance"


class TestResultViewSet(ModelViewSet):
    queryset = TestResultSelector().result_list()
    permission_classes = [permissions.IsAdminOrForbidArchiveUpdate]
    serializer_class = TestResultSerializer
    filter_backends = [TestyFilterBackend]
    filterset_class = TestResultFilter

    def perform_update(self, serializer: TestResultSerializer):
        serializer.instance = TestResultService().result_update(serializer.instance, serializer.validated_data)

    def perform_create(self, serializer: TestResultSerializer):
        request = serializer.context.get('request')
        serializer.instance = TestResultService().result_create(serializer.validated_data, request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TestResultInputSerializer
        return TestResultSerializer


class TestResultChoicesView(APIView):

    def get(self, request):
        choices = [{'id': status_id, 'status': status_name} for status_id, status_name in TestStatuses.choices]
        return Response(choices, status=status.HTTP_200_OK)
