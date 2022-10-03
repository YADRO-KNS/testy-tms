from rest_framework.viewsets import ModelViewSet

from tests_description.api.v1.serializers import (TestCaseSerializer,
                                                  TestSuiteSerializer)
from tests_description.models import TestCase, TestSuite


class TestSuiteViewSet(ModelViewSet):
    queryset = TestSuite.objects.all()
    serializer_class = TestSuiteSerializer


class TestCaseViewSet(ModelViewSet):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
