from rest_framework.viewsets import ModelViewSet
from tests_representation.api.v1.serializers import (ParameterSerializer,
                                                     TestPlanSerializer,
                                                     TestResultSerializer,
                                                     TestSerializer,
                                                     TestStatusSerializer)
from tests_representation.models import (Parameter, Test, TestPlan, TestResult,
                                         TestStatus)
from tests_representation.services.plans import TestPlanDto, TestPlanService
from tests_representation.services.results import (TestResultDto,
                                                   TestResultService)
from tests_representation.services.tests import TestDto, TestService

from tms.utils.mixins import DtoMixin


class ParameterViewSet(ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer


class TestPlanViewSet(ModelViewSet, DtoMixin):
    queryset = TestPlan.objects.all()
    serializer_class = TestPlanSerializer
    dto_class = TestPlanDto

    def perform_create(self, serializer: TestPlanSerializer):
        dto = self.build_dto_from_validated_data(serializer.validated_data)
        serializer.instance = TestPlanService().plan_create(dto)

    def perform_update(self, serializer: TestPlanSerializer):
        dto = self.build_dto_from_validated_data(serializer.validated_data)
        plan = serializer.instance
        serializer.instance = TestPlanService().plan_update(plan, dto)

    def perform_destroy(self, plan: TestPlan):
        TestPlanService().plan_delete(plan)


class TestViewSet(ModelViewSet, DtoMixin):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    dto_class = TestDto

    def perform_create(self, serializer: TestSerializer):
        dto = self.build_dto_from_validated_data(serializer.validated_data)
        serializer.instance = TestService().test_create(dto)

    def perform_update(self, serializer: TestSerializer):
        dto = self.build_dto_from_validated_data(serializer.validated_data)
        test = serializer.instance
        serializer.instance = TestService().test_update(test, dto)

    def perform_destroy(self, test: Test):
        TestService().test_delete(test)


class TestResultViewSet(ModelViewSet, DtoMixin):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    dto_class = TestResultDto

    def perform_create(self, serializer: TestPlanSerializer):
        dto = self.build_dto_from_validated_data(serializer.validated_data)
        serializer.instance = TestResultService().result_create(dto)

    def perform_update(self, serializer: TestPlanSerializer):
        dto = self.build_dto_from_validated_data(serializer.validated_data)
        result = serializer.instance
        serializer.instance = TestResultService().result_update(result, dto)

    def perform_destroy(self, result: TestResult):
        TestResultService().result_delete(result)


class TestStatusViewSet(ModelViewSet):
    queryset = TestStatus.objects.all()
    serializer_class = TestStatusSerializer
