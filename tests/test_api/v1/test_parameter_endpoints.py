# TestY TMS - Test Management System
# Copyright (C) 2022 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.

import json
from http import HTTPStatus

import pytest
from django.forms import model_to_dict
from tests_representation.models import Parameter

from tests import constants
from tests.commons import RequestType
from tests.error_messages import REQUIRED_FIELD_MSG


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
