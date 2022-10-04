from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer
from tests_description.models import TestCase, TestSuite


class TestSuiteSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testsuite-detail')

    class Meta:
        model = TestSuite
        fields = ('id', 'name', 'project', 'parent', 'url')


class TestCaseSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testcase-detail')

    class Meta:
        model = TestCase
        fields = ('id', 'name', 'project', 'suite', 'setup', 'scenario', 'teardown', 'estimate', 'url')
