from typing import Dict

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


class AttachmentsViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = AttachmentSelector().attachment_list()
    serializer_class = AttachmentSerializer

    def create(self, request, *args, **kwargs):
        formatted_file_dicts = []
        for file in request.FILES.getlist('file'):
            formatted_data = {
                'filename': file.get('name'),
                'content_type': file.get('content_type'),
                'size': file.get('size'),
                'user': request.user,
                'file': file
            }
            verified_result = self._verify_parents(file)
            if isinstance(verified_result, Response):
                return verified_result
            formatted_file_dicts.append(formatted_data.update(verified_result))

        for file_dict in formatted_file_dicts:
            serializer = self.get_serializer(data=file_dict)
            serializer.is_valid(raise_exception=True)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def _verify_parents(self, file: Dict):
        parent_field_names = ['case', 'result', 'test_plan']
        parent_dict = {}
        for field_name in parent_field_names:
            field_value = file.get(field_name)
            if field_value:
                parent_dict[field_name] = field_value
                if len(parent_dict):
                    return Response(
                        {'details': 'Only one parent allowed case/result/plan'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        if not parent_dict:
            return Response({'details': 'No parent was provided(case/result/plan)'}, status=status.HTTP_400_BAD_REQUEST)
        return parent_dict
