from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer
from tests_representation.models import (Parameter, Test, TestPlan, TestResult,
                                         TestStatus)


class ParameterSerializer(ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'project', 'group_name', 'data')


class TestPlanSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testplan-detail')

    class Meta:
        model = TestPlan
        fields = ('id', 'parent', 'started_at', 'due_date', 'finished_at', 'is_archive', 'url')


class TestSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:test-detail')

    class Meta:
        model = Test
        fields = ('id', 'case', 'plan', 'user', 'is_archive', 'created_at', 'updated_at', 'url')


class TestResultSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testresult-detail')

    class Meta:
        model = TestResult
        fields = ('id', 'test', 'status', 'comment', 'user', 'is_archive', 'url', 'created_at', 'updated_at')


class TestStatusSerializer(ModelSerializer):
    class Meta:
        model = TestStatus
        fields = ('id', 'name', 'status_code')
