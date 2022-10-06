from rest_framework.viewsets import ModelViewSet

from tests_description.api.v1.serializers import (TestCaseSerializer,
                                                  TestSuiteSerializer)
from tests_description.selectors.cases import TestCaseSelector
from tests_description.selectors.suites import TestSuiteSelector
from tests_description.services.cases import TestCaseService
from tests_description.services.suites import TestSuiteService


class TestCaseViewSet(ModelViewSet):
    queryset = TestCaseSelector().case_list()
    serializer_class = TestCaseSerializer

    def perform_create(self, serializer: TestCaseSerializer):
        serializer.instance = TestCaseService().case_create(serializer.validated_data)

    def perform_update(self, serializer: TestCaseSerializer):
        serializer.instance = TestCaseService().case_update(serializer.instance, serializer.validated_data)


class TestSuiteViewSet(ModelViewSet):
    queryset = TestSuiteSelector().suite_list()
    serializer_class = TestSuiteSerializer

    def perform_create(self, serializer: TestSuiteSerializer):
        serializer.instance = TestSuiteService().suite_create(serializer.validated_data)

    def perform_update(self, serializer: TestSuiteSerializer):
        serializer.instance = TestSuiteService().suite_update(serializer.instance, serializer.validated_data)
