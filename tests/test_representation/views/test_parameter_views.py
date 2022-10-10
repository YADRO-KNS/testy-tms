import json
from http import HTTPStatus

import constants
import pytest
from factories import ParameterFactory
from tests_representation.models import Parameter


@pytest.mark.django_db
class TestParameterView:

    def test_parameter_retrieve(self, api_client, authorized_superuser):
        number_of_parameters = 10
        expected_parameters_names_list = []
        for _ in range(number_of_parameters):
            expected_parameters_names_list.append(ParameterFactory.create().id)

        response = api_client.get(constants.PARAMETERS_URL)
        for parameter in json.loads(response.content):
            assert parameter.get('id') in expected_parameters_names_list, f'Name "{parameter.get("id")}" ' \
                                                                          'was not in list of expected names'
        assert response.status_code == HTTPStatus.OK, f'Expected response code "{HTTPStatus.OK}", ' \
                                                      f'actual: "{response.status_code}"'

    def test_parameter_creation(self, api_client, authorized_superuser, project, test_suite):
        expected_number_of_cases = 1
        parameter_json = {
            'group_name': constants.PARAMETER_GROUP_NAME,
            'project': project.id,
            'data': constants.PARAMETER_DATA
        }
        response = api_client.post(constants.PARAMETERS_URL, data=parameter_json)
        assert response.status_code == HTTPStatus.CREATED, f'Expected response code "{HTTPStatus.CREATED}", ' \
                                                           f'actual: "{response.status_code}"'
        assert Parameter.objects.count() == expected_number_of_cases, f'Expected number of users ' \
                                                                      f'"{expected_number_of_cases}"' \
                                                                      f'actual: "{Parameter.objects.count()}"'

    def test_parameter_update(self, api_client, authorized_superuser, parameter):
        new_data = 'new_data'
        parameter_json = {
            'id': parameter.id,
            'data': new_data
        }
        response = api_client.patch(constants.SINGLE_PARAMETER_URL.format(id=parameter.id), data=parameter_json)
        assert response.status_code == HTTPStatus.OK, f'Expected response code "{HTTPStatus.OK}", ' \
                                                      f'actual: "{response.status_code}"'
        actual_data = Parameter.objects.get(pk=parameter.id).data
        assert actual_data == new_data, f'Username does not match. Expected name "{new_data}", actual: "{actual_data}"'

    def test_parameter_delete(self, api_client, authorized_superuser, parameter):
        assert Parameter.objects.count() == 1
        response = api_client.delete(constants.SINGLE_PARAMETER_URL.format(id=parameter.id))
        assert response.status_code == HTTPStatus.NO_CONTENT, f'Expected response code "{HTTPStatus.NO_CONTENT}", ' \
                                                              f'actual: "{response.status_code}"'
        assert not Parameter.objects.filter(pk=parameter.id), f'Parameter with id "{parameter.id}" was not deleted.'
