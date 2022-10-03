from rest_framework.serializers import ModelSerializer

from tests_description.models import TestCase, TestSuite


class TestSuiteSerializer(ModelSerializer):
    class Meta:
        model = TestSuite
        fields = ('id', 'name')


class TestCaseSerializer(ModelSerializer):
    class Meta:
        model = TestCase
        fields = ('id', 'name')
