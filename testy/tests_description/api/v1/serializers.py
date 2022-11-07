
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer
from tests_description.models import TestCase, TestSuite


class TestCaseSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testcase-detail')

    class Meta:
        model = TestCase
        fields = ('id', 'name', 'project', 'suite', 'setup', 'scenario', 'teardown', 'estimate', 'url')


class TestSuiteTreeSerializer(ModelSerializer):
    children = SerializerMethodField()
    test_cases = SerializerMethodField('get_test_case_serializer')

    class Meta:
        model = TestSuite
        fields = ('id', 'name', 'level', 'children', 'test_cases')

    def get_children(self, value):
        return self.__class__(value.get_children(), many=True).data

    def get_test_case_serializer(self, obj):
        serializer_context = {'request': self.context.get('request')}
        test_cases = TestCase.objects.all().filter(suite=obj)
        serializer = TestCaseSerializer(test_cases, many=True, context=serializer_context)
        return serializer.data


class TestSuiteSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testsuite-detail')
    test_cases = TestCaseSerializer(many=True, read_only=True)

    class Meta:
        model = TestSuite
        fields = ('id', 'name', 'parent', 'project', 'url', 'test_cases',)
