from rest_framework.viewsets import ModelViewSet
from tests_representation.api.v1.serializers import (ParameterSerializer,
                                                     TestPlanSerializer,
                                                     TestSerializer)
from tests_representation.models import Parameter, Test, TestPlan


class ParameterViewSet(ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer


class TestPlanViewSet(ModelViewSet):
    queryset = TestPlan.objects.all()
    serializer_class = TestPlanSerializer


class TestViewSet(ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
