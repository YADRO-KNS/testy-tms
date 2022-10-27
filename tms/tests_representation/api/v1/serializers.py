from rest_framework.relations import HyperlinkedIdentityField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from tests_description.selectors.cases import TestCaseSelector
from tests_representation.models import Parameter, Test, TestPlan, TestResult
from tests_representation.selectors.parameters import ParameterSelector
from tests_representation.models import Attachment, Parameter, Test, TestResult


class ParameterSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:parameter-detail')

    class Meta:
        model = Parameter
        fields = ('id', 'project', 'data', 'group_name', 'url')


class TestPlanUpdateSerializer(ModelSerializer):
    test_cases = PrimaryKeyRelatedField(queryset=TestCaseSelector().case_list(), many=True, required=False)

    class Meta:
        model = TestPlan
        fields = (
            'id', 'name', 'parent', 'test_cases', 'started_at', 'due_date', 'finished_at', 'is_archive', 'project',
        )


class TestPlanInputSerializer(ModelSerializer):
    test_cases = PrimaryKeyRelatedField(queryset=TestCaseSelector().case_list(), many=True, required=False)
    parameters = PrimaryKeyRelatedField(queryset=ParameterSelector().parameter_list(), many=True, required=False)

    class Meta:
        model = TestPlan
        fields = (
            'id', 'name', 'parent', 'test_cases', 'parameters', 'started_at', 'due_date', 'finished_at', 'is_archive',
            'project',
        )


class TestPlanOutputSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testplan-detail')

    class Meta:
        model = TestPlan
        fields = (
            'id', 'name', 'parent', 'parameters', 'started_at', 'due_date', 'finished_at', 'is_archive',
            'url', 'child_test_plans', 'tests', 'project',
        )


class TestSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:test-detail')

    class Meta:
        model = Test
        fields = ('id', 'project', 'case', 'plan', 'user', 'is_archive', 'created_at', 'updated_at', 'url')

        read_only_fields = ('project',)


class TestResultSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testresult-detail')

    class Meta:
        model = TestResult
        fields = (
            'id', 'project', 'status', 'test', 'user', 'comment', 'is_archive', 'test_case_version', 'created_at',
            'updated_at', 'url'
        )

        read_only_fields = ('test_case_version', 'project', 'test')


class AttachmentSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:attachment-detail')

    class Meta:
        model = Attachment
        fields = (
            'project', 'name', 'filename', 'content_type', 'size', 'case', 'plan', 'result', 'user', 'file', 'url'
        )

        read_only_fields = ('project', 'name', 'filename', 'content_type', 'size', 'user', 'url')
