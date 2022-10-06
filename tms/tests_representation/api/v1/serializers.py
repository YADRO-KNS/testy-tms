from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer

from tests_representation.models import Parameter, Test, TestResult, TestStatus


class ParameterSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:parameter-detail')

    class Meta:
        model = Parameter
        fields = ('id', 'project', 'data', 'group_name', 'url')


class TestSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:test-detail')

    class Meta:
        model = Test
        fields = ('id', 'case', 'plan', 'user', 'is_archive', 'created_at', 'updated_at', 'url')


class TestStatusSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:teststatus-detail')

    class Meta:
        model = TestStatus
        fields = ('id', 'name', 'status_code', 'url')


class TestResultSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testresult-detail')

    class Meta:
        model = TestResult
        fields = (
            'id', 'status', 'test', 'user', 'comment', 'is_archive', 'test_case_version', 'created_at', 'updated_at',
            'url'
        )
