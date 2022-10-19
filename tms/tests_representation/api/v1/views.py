from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from tests_representation.api.v1.serializers import (
    ParameterSerializer,
    TestPlanInputSerializer,
    TestPlanOutputSerializer,
    TestPlanUpdateSerializer,
    TestResultSerializer,
    TestSerializer,
)
from tests_representation.selectors.parameters import ParameterSelector
from tests_representation.selectors.results import TestResultSelector
from tests_representation.selectors.testplan import TestPlanSelector
from tests_representation.selectors.tests import TestSelector
from tests_representation.services.parameters import ParameterService
from tests_representation.services.results import TestResultService
from tests_representation.services.testplans import TestPLanService
from tests_representation.services.tests import TestService


class ParameterViewSet(ModelViewSet):
    queryset = ParameterSelector().parameter_list()
    serializer_class = ParameterSerializer

    def perform_create(self, serializer: ParameterSerializer):
        serializer.instance = ParameterService().parameter_create(serializer.validated_data)

    def perform_update(self, serializer: ParameterSerializer):
        serializer.instance = ParameterService().parameter_update(serializer.instance, serializer.validated_data)


class TestPLanListView(APIView):
    def get_view_name(self):
        return "Test Plan List"

    def get(self, request):
        qs = TestPlanSelector().testplan_list()
        serializer = TestPlanOutputSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = TestPlanInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        test_plans = TestPLanService().testplan_create(serializer.validated_data)
        return Response(TestPlanOutputSerializer(test_plans, many=True, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)


class TestPLanDetailView(APIView):
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
        serializer = TestPlanUpdateSerializer(data=request.data, instance=test_plan, context={"request": request},
                                              partial=True)
        serializer.is_valid(raise_exception=True)
        test_plan = TestPLanService().testplan_update(test_plan=test_plan, data=serializer.validated_data)
        return Response(TestPlanOutputSerializer(test_plan, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        test_plan = self.get_object(pk)
        TestPLanService().testplan_delete(test_plan=test_plan)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TestListViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = TestSelector().test_list()
    serializer_class = TestSerializer

    def get_view_name(self):
        return "Test List"

    def perform_update(self, serializer: TestSerializer):
        serializer.instance = TestService().test_update(serializer.instance, serializer.validated_data)


class TestDetailViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = TestSelector().test_list()
    serializer_class = TestSerializer

    def get_view_name(self):
        return "Test Instance"


class TestResultViewSet(ModelViewSet):
    queryset = TestResultSelector().result_list()
    serializer_class = TestResultSerializer

    def perform_create(self, serializer: TestResultSerializer):
        serializer.instance = TestResultService().result_create(serializer.validated_data)

    def perform_update(self, serializer: TestResultSerializer):
        serializer.instance = TestResultService().result_update(serializer.instance, serializer.validated_data)
