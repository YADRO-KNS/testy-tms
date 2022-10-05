from rest_framework.viewsets import ModelViewSet
from tests_representation.api.v1.serializers import (ParameterSerializer,
                                                     TestPlanSerializer,
                                                     TestResultSerializer,
                                                     TestSerializer,
                                                     TestStatusSerializer)
from tests_representation.selectors.parameters import ParameterSelector
from tests_representation.selectors.plans import TestPlanSelector
from tests_representation.selectors.results import TestResultSelector
from tests_representation.selectors.statuses import TestStatusSelector
from tests_representation.selectors.tests import TestSelector
from tests_representation.services.parameters import ParameterService
from tests_representation.services.plans import TestPlanService
from tests_representation.services.results import TestResultService
from tests_representation.services.statuses import TestStatusService
from tests_representation.services.tests import TestService


class ParameterViewSet(ModelViewSet):
    queryset = ParameterSelector().parameter_list()
    serializer_class = ParameterSerializer

    def perform_create(self, serializer: ParameterSerializer):
        serializer.instance = ParameterService().parameter_create(serializer.validated_data)

    def perform_update(self, serializer: TestPlanSerializer):
        serializer.instance = ParameterService().parameter_update(serializer.instance, serializer.validated_data)


class TestPlanViewSet(ModelViewSet):
    queryset = TestPlanSelector().plan_list()
    serializer_class = TestPlanSerializer

    def perform_create(self, serializer: TestPlanSerializer):
        serializer.instance = TestPlanService().plan_create(serializer.validated_data)

    def perform_update(self, serializer: TestPlanSerializer):
        serializer.instance = TestPlanService().plan_update(serializer.instance, serializer.validated_data)


class TestViewSet(ModelViewSet):
    queryset = TestSelector().test_list()
    serializer_class = TestSerializer

    def perform_create(self, serializer: TestSerializer):
        serializer.instance = TestService().test_create(serializer.validated_data)

    def perform_update(self, serializer: TestSerializer):
        serializer.instance = TestService().test_update(serializer.instance, serializer.validated_data)


class TestResultViewSet(ModelViewSet):
    queryset = TestResultSelector().result_list()
    serializer_class = TestResultSerializer

    def perform_create(self, serializer: TestResultSerializer):
        serializer.instance = TestResultService().result_create(serializer.validated_data)

    def perform_update(self, serializer: TestResultSerializer):
        serializer.instance = TestResultService().result_update(serializer.instance, serializer.validated_data)


class TestStatusViewSet(ModelViewSet):
    queryset = TestStatusSelector().status_list()
    serializer_class = TestStatusSerializer

    def perform_create(self, serializer: TestStatusSerializer):
        serializer.instance = TestStatusService().status_create(serializer.validated_data)

    def perform_update(self, serializer: TestStatusSerializer):
        serializer.instance = TestStatusService().status_update(serializer.instance, serializer.validated_data)
