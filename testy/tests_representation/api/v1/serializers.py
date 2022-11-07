
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from tests_description.api.v1.serializers import TestCaseSerializer
from tests_description.selectors.cases import TestCaseSelector
from tests_representation.models import Parameter, Test, TestPlan, TestResult
from tests_representation.selectors.parameters import ParameterSelector
from tests_representation.selectors.results import TestResultSelector


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


class TestPlanTreeSerializer(ModelSerializer):
    children = SerializerMethodField()
    title = SerializerMethodField()

    class Meta:
        model = TestPlan
        fields = ('id', 'name', 'level', 'children', 'title')

    def get_title(self, instance):
        if instance.parameters is None:
            return instance.name
        parameters = ParameterSelector().parameter_name_list_by_ids(instance.parameters)
        return '{0} [{1}]'.format(instance.name, ', '.join(parameters))

    def get_children(self, value):
        return self.__class__(value.get_children(), many=True).data


class TestPlanTestResultSerializer(ModelSerializer):
    status = SerializerMethodField()
    updated_at = SerializerMethodField()

    class Meta:
        model = TestResult
        fields = (
            'id', 'status', 'comment', 'test_case_version', 'created_at', 'updated_at'
        )

    def get_status(self, instance):
        return instance.get_status_display()

    def get_updated_at(self, instance):
        return instance.updated_at.strftime("%d.%m.%Y %H:%M:%S")


class TestPlanTestSerializer(ModelSerializer):
    case = TestCaseSerializer()
    current_result = SerializerMethodField()
    test_results = TestPlanTestResultSerializer(many=True, read_only=True)

    def get_test_results(self, instance):
        return TestResultSelector().result_list_by_test_id(instance.id)

    class Meta:
        model = Test
        fields = ('id', 'case', 'plan', 'is_archive', 'created_at', 'updated_at', 'test_results',
                  'current_result')

    def get_current_result(self, instance):
        if instance.test_results.last():
            return instance.test_results.last().get_status_display()
        return None


class TestPlanOutputSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testplan-detail')
    tests = TestPlanTestSerializer(many=True, read_only=True)
    title = SerializerMethodField()

    class Meta:
        model = TestPlan
        fields = (
            'id', 'name', 'parent', 'parameters', 'started_at', 'due_date', 'finished_at', 'is_archive',
            'tests', 'project', 'child_test_plans', 'url', 'title'
        )

    def get_title(self, instance):
        if instance.parameters is None:
            return instance.name
        parameters = ParameterSelector().parameter_name_list_by_ids(instance.parameters)
        return '{0} [{1}]'.format(instance.name, ', '.join(parameters))
