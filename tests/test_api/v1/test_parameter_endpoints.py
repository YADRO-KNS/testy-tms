import json
from http import HTTPStatus

import pytest
from django.forms import model_to_dict

from tests.error_messages import REQUIRED_FIELD_MSG
from tests_representation.models import Parameter

from tests import constants
from tests.commons import RequestType


@pytest.mark.django_db
class TestParameterEndpoints:
    view_name_list = 'api:v1:parameter-list'
    view_name_detail = 'api:v1:parameter-detail'

    def test_list(self, api_client, authorized_superuser, parameter_factory):
        expected_instances = []
        for _ in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
            expected_instances.append(model_to_dict(parameter_factory()))

        response = api_client.send_request(self.view_name_list)

        for instance in json.loads(response.content):
            instance.pop('url')
            assert instance in expected_instances

    def test_retrieve(self, api_client, authorized_superuser, parameter):
        expected_parameter_dict = model_to_dict(parameter)
        response = api_client.send_request(self.view_name_detail, reverse_kwargs={'pk': parameter.pk})
        actual_model_dict = json.loads(response.content)
        actual_model_dict.pop('url')
        assert actual_model_dict == expected_parameter_dict, 'Actual model dict is different from expected'

    def test_creation(self, api_client, authorized_superuser, project):
        expected_number_of_parameters = 1
        parameter_dict = {
            'group_name': constants.PARAMETER_GROUP_NAME,
            'project': project.id,
            'data': constants.PARAMETER_DATA
        }
        api_client.send_request(self.view_name_list, parameter_dict, HTTPStatus.CREATED, RequestType.POST)
        assert Parameter.objects.count() == expected_number_of_parameters, f'Expected number of parameters is ' \
                                                                           f'"{expected_number_of_parameters}"' \
                                                                           f'actual: "{Parameter.objects.count()}"'

    def test_partial_update(self, api_client, authorized_superuser, parameter):
        new_data = 'new_data'
        parameter_dict = {
            'id': parameter.id,
            'data': new_data
        }
        api_client.send_request(
            self.view_name_detail,
            reverse_kwargs={'pk': parameter.pk},
            request_type=RequestType.PATCH,
            data=parameter_dict
        )
        actual_data = Parameter.objects.get(pk=parameter.id).data
        assert actual_data == new_data, f'New data does not match. Expected data "{new_data}", actual: "{actual_data}"'

    @pytest.mark.parametrize('expected_status', [HTTPStatus.OK, HTTPStatus.BAD_REQUEST])
    def test_update(self, api_client, authorized_superuser, parameter, expected_status, project):
        new_data = 'new_data'
        parameter_dict = {
            'id': parameter.id,
            'data': new_data
        }
        if expected_status == HTTPStatus.OK:
            parameter_dict['project'] = project.id
            parameter_dict['group_name'] = parameter.group_name
        response = api_client.send_request(
            self.view_name_detail,
            reverse_kwargs={'pk': parameter.pk},
            request_type=RequestType.PUT,
            expected_status=expected_status,
            data=parameter_dict
        )
        if expected_status == HTTPStatus.OK:
            actual_data = Parameter.objects.get(pk=parameter.id).data
            assert actual_data == new_data, f'Parameter data do not match. Expected name "{actual_data}", ' \
                                            f'actual: "{new_data}"'
        else:
            assert json.loads(response.content)['group_name'][0] == REQUIRED_FIELD_MSG
            assert json.loads(response.content)['project'][0] == REQUIRED_FIELD_MSG

    def test_delete(self, api_client, authorized_superuser, parameter):
        assert Parameter.objects.count() == 1, 'Parameter was not created'
        api_client.send_request(
            self.view_name_detail,
            expected_status=HTTPStatus.NO_CONTENT,
            request_type=RequestType.DELETE,
            reverse_kwargs={'pk': parameter.pk}
        )
        assert not Parameter.objects.count(), f'Parameter with id "{parameter.id}" was not deleted.'
