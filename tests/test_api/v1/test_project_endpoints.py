
import json
from http import HTTPStatus

import pytest
from core.models import Project
from django.forms import model_to_dict
from tests_description.models import TestCase
from tests_representation.choices import TestStatuses
from tests_representation.models import Parameter, TestResult

from tests import constants
from tests.commons import RequestType
from tests.error_messages import REQUIRED_FIELD_MSG


@pytest.mark.django_db
class TestProjectEndpoints:
    view_name_list = 'api:v1:project-list'
    view_name_detail = 'api:v1:project-detail'

    def test_list(self, api_client, authorized_superuser, project_factory):
        expected_instances = []
        for _ in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
            expected_instances.append(model_to_dict(project_factory()))

        response = api_client.send_request(self.view_name_list)
        for instance in json.loads(response.content):
            instance.pop('url')
            assert instance in expected_instances

    def test_retrieve(self, api_client, authorized_superuser, project):
        expected_dict = model_to_dict(project)
        response = api_client.send_request(self.view_name_detail, reverse_kwargs={'pk': project.pk})
        actual_dict = json.loads(response.content)
        actual_dict.pop('url')
        assert actual_dict == expected_dict

    def test_creation(self, api_client, authorized_superuser):
        expected_number_of_parameters = 1
        project_dict = {
            'name': constants.PROJECT_NAME,
            'description': constants.DESCRIPTION
        }
        api_client.send_request(self.view_name_list, project_dict, HTTPStatus.CREATED, RequestType.POST)
        assert Project.objects.count() == expected_number_of_parameters, f'Expected number of projects is ' \
                                                                         f'"{expected_number_of_parameters}"' \
                                                                         f'actual: "{Parameter.objects.count()}"'

    def test_partial_update(self, api_client, authorized_superuser, project):
        new_name = 'new_name'
        project_dict = {
            'id': project.id,
            'name': new_name,
        }
        api_client.send_request(
            self.view_name_detail,
            reverse_kwargs={'pk': project.pk},
            request_type=RequestType.PATCH,
            data=project_dict
        )
        actual_name = Project.objects.get(pk=project.id).name
        assert actual_name == new_name, f'New name does not match. Expected name "{new_name}", actual: "{actual_name}"'

    @pytest.mark.parametrize('expected_status', [HTTPStatus.OK, HTTPStatus.BAD_REQUEST])
    def test_update(self, api_client, authorized_superuser, project, expected_status):
        new_name = 'new_name'
        project_dict = {
            'id': project.id,
        }
        if expected_status == HTTPStatus.OK:
            project_dict['name'] = new_name
        response = api_client.send_request(
            self.view_name_detail,
            reverse_kwargs={'pk': project.pk},
            request_type=RequestType.PUT,
            expected_status=expected_status,
            data=project_dict
        )
        if expected_status == HTTPStatus.OK:
            actual_name = Project.objects.get(pk=project.id).name
            assert actual_name == new_name, f'Project name do not match. Expected name "{actual_name}", ' \
                                            f'actual: "{new_name}"'
        else:
            assert json.loads(response.content)['name'][0] == REQUIRED_FIELD_MSG

    def test_delete(self, api_client, authorized_superuser, project):
        assert Project.objects.count() == 1, 'Project was not created'
        api_client.send_request(
            self.view_name_detail,
            expected_status=HTTPStatus.NO_CONTENT,
            request_type=RequestType.DELETE,
            reverse_kwargs={'pk': project.pk}
        )
        assert not Project.objects.count(), f'Project with id "{project.id}" was not deleted.'

    def test_valid_project_assignation(self, api_client, authorized_superuser, user, test):
        result_dict = {
            'status': TestStatuses.UNTESTED,
            'test': test.id,
            'user': user.id,
            'comment': constants.TEST_COMMENT,
        }
        api_client.send_request(
            'api:v1:results-by-test',
            result_dict,
            HTTPStatus.CREATED,
            RequestType.POST,
            reverse_kwargs={'pk': test.id}
        )

        expected_project = TestCase.objects.all()[0].project

        result_project = TestResult.objects.all()[0].project

        assert test.project == expected_project, f'Test was not created with correct project, ' \
                                                 f'expected project: {expected_project}' \
                                                 f'actual project: {test.project}'
        assert result_project == expected_project, f'Test result was not created with correct project, ' \
                                                   f'expected project: {expected_project}' \
                                                   f'actual project: {result_project}'
