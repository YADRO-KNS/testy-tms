from rest_framework.viewsets import ModelViewSet
from tests_description.api.v1.serializers import (TestCaseSerializer,
                                                  TestSuiteSerializer)
from tests_description.models import TestCase, TestSuite
from tests_description.services.cases import TestCaseDto, TestCaseService
from tests_description.services.suites import TestSuiteDto, TestSuiteService

from tms.utils.mixins import DtoMixin


class TestSuiteViewSet(ModelViewSet, DtoMixin):
    queryset = TestSuite.objects.all()
    serializer_class = TestSuiteSerializer
    dto_class = TestSuiteDto

    def perform_create(self, serializer: TestSuiteSerializer):
        dto = self.build_dto_from_validated_data(serializer.validated_data)
        serializer.instance = TestSuiteService().suite_create(dto)

    def perform_update(self, serializer: TestSuiteSerializer):
        dto = self.build_dto_from_validated_data(serializer.validated_data)
        plan = serializer.instance
        serializer.instance = TestSuiteService().suite_update(plan, dto)

    def perform_destroy(self, suite: TestSuite):
        TestSuiteService().suite_delete(suite)


class TestCaseViewSet(ModelViewSet, DtoMixin):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    dto_class = TestCaseDto

    def perform_create(self, serializer: TestCaseSerializer):
        dto = self.build_dto_from_validated_data(serializer.validated_data)
        serializer.instance = TestCaseService().case_create(dto)

    def perform_update(self, serializer: TestCaseSerializer):
        dto = self.build_dto_from_validated_data(serializer.validated_data)
        case = serializer.instance
        serializer.instance = TestCaseService().case_update(case, dto)

    def perform_destroy(self, case: TestCase):
        TestCaseService().case_delete(case)
