from rest_framework.serializers import ModelSerializer
from tests_representation.models import Parameter, Test, TestPlan


class ParameterSerializer(ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'project', 'group_name')


class TestPlanSerializer(ModelSerializer):
    class Meta:
        model = TestPlan
        fields = ('id',)


class TestSerializer(ModelSerializer):
    class Meta:
        model = Test
        fields = ('id',)
