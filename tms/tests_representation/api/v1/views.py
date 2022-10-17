from rest_framework import mixins, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from tests_representation.api.v1.serializers import ParameterSerializer, TestResultSerializer, TestSerializer
from tests_representation.models import Test
from tests_representation.selectors.parameters import ParameterSelector
from tests_representation.selectors.results import TestResultSelector
from tests_representation.selectors.tests import TestSelector
from tests_representation.services.parameters import ParameterService
from tests_representation.services.results import TestResultService
from tests_representation.services.tests import TestService


class ParameterViewSet(ModelViewSet):
    queryset = ParameterSelector().parameter_list()
    serializer_class = ParameterSerializer

    def perform_create(self, serializer: ParameterSerializer):
        serializer.instance = ParameterService().parameter_create(serializer.validated_data)

    def perform_update(self, serializer: ParameterSerializer):
        serializer.instance = ParameterService().parameter_update(serializer.instance, serializer.validated_data)


class TestListViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = TestSelector().test_list()
    serializer_class = TestSerializer

    def get_view_name(self):
        return "Test List"

    def perform_update(self, serializer: TestSerializer):
        serializer.instance = TestService().test_update(serializer.instance, serializer.validated_data)


class TestDetailViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = TestSelector().test_list()
    serializer_class = TestSerializer

    def get_view_name(self):
        return "Test Instance"


class TestResultViewSet(ModelViewSet):
    queryset = TestResultSelector().result_list()
    serializer_class = TestResultSerializer

    def perform_create(self, serializer: TestResultSerializer):
        serializer.instance = TestResultService().result_create(serializer.validated_data)

    def perform_update(self, serializer: TestResultSerializer):
        serializer.instance = TestResultService().result_update(serializer.instance, serializer.validated_data)


class AddTestResultToTest(CreateAPIView):
    serializer_class = TestResultSerializer

    def post(self, request, *args, **kwargs):
        test_id = kwargs['test_id']
        if not Test.objects.get(pk=test_id):
            return Response(
                {'message': f'No test with id "{test_id}" was found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        request.data._mutable = True
        request.data.update({'test': kwargs['test_id']})
        request.data._mutable = False
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.instance = TestResultService().result_create(serializer.validated_data)


class TestResultByTest(ListAPIView):
    serializer_class = TestResultSerializer

    def get_queryset(self):
        return TestResultSelector().result_list_by_test_id(self.kwargs.get('test_id'))
