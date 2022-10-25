from typing import Any, Dict

from rest_framework import status
from rest_framework.response import Response

from tests_description.models import TestCase
from tests_representation.models import Parameter, Attachment


class AttachmentService:
    non_side_effect_fields = ['project', 'name', 'filename', 'content_type', 'size', 'test_plan', 'case', 'result',
                              'user', 'file']

    def attachment_create(self, data: Dict[str, Any]) -> Attachment:
        return Attachment.model_create(
            fields=self.non_side_effect_fields,
            data=data,
        )

    def attachment_update(self, parameter: Attachment, data: Dict[str, Any]) -> Attachment:
        parameter, _ = parameter.model_update(
            fields=self.non_side_effect_fields,
            data=data,
        )
        return parameter

    def format_file(self, request):
        formatted_file_dicts = []
        response = None
        for file in request.FILES.getlist('file'):
            formatted_data = {
                'name': file.name.split('.')[0],
                'filename': file.name,
                'content_type': file.content_type,
                'size': file.size,
                'user': request.user,
                'file': file
            }
            parent_dict, new_response = self._verify_parents(request.POST)
            if new_response:
                response = new_response
            formatted_data.update(parent_dict)
            formatted_file_dicts.append(formatted_data)
        return formatted_file_dicts, response

    def _verify_parents(self, post_data):
        parent_field_names = ['case', 'result', 'test_plan']
        parent_dict = {}
        project = None
        for field_name in parent_field_names:
            field_value = post_data.get(field_name)
            if field_value:
                parent_dict[field_name], new_project = field_value
                new_project = self._get_parent_project(field_name, field_value)
                if project and new_project and not project == new_project:
                    return dict(), Response(
                        {'details': f'several parents have different project id, for file {post_data.get("name")}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        parent_dict['project'] = project
        return parent_dict, None

    def _get_parent_project(self, field_name: str, field_value):
        if field_name == 'case':
            case = TestCase.objects.get(pk=field_value)
            project = case.project
            return case, project
