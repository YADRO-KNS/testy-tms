from django.forms import model_to_dict
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from tests_representation.api.v1.serializers import (
    AttachmentSerializer,
    ParameterSerializer,
    TestResultSerializer,
    TestSerializer,
)
from tests_representation.selectors.attachments import AttachmentSelector
from tests_representation.selectors.parameters import ParameterSelector
from tests_representation.selectors.results import TestResultSelector
from tests_representation.selectors.tests import TestSelector
from tests_representation.services.attachments import AttachmentService
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

    @action(detail=False, methods=['POST'])
    def add_result(self, request, pk):
        serializer = TestResultSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        result = TestResultService().result_create(serializer.validated_data, pk)
        return Response(model_to_dict(result), status=status.HTTP_201_CREATED)

    @action(detail=False)
    def results_by_test(self, request, pk):
        queryset = self.filter_queryset(TestResultSelector().result_list_by_test_id(pk))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TestResultSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = TestResultSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class TestResultViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = TestResultSelector().result_list()
    serializer_class = TestResultSerializer

    def perform_update(self, serializer: TestResultSerializer):
        serializer.instance = TestResultService().result_update(serializer.instance, serializer.validated_data)


class AttachmentViewSet(ModelViewSet):
    queryset = AttachmentSelector().attachment_list()
    serializer_class = AttachmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attachments = AttachmentService().attachment_create(serializer.validated_data, request)
        data = [self.get_serializer(attachment, context={'request': request}).data for attachment in attachments]
        return Response(data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        serializer.instance = TestResultService().result_update(serializer.instance, serializer.validated_data)
