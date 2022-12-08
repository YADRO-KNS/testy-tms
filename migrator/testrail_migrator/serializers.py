from rest_framework.serializers import ModelSerializer

from tests_representation.models import Parameter


class ParameterSerializer(ModelSerializer):

    class Meta:
        model = Parameter
        fields = ('id', 'project', 'data', 'group_name')