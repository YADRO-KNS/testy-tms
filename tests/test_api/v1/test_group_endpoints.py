# TMS - Test Management System
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
from users.models import Group

from tests import constants
from tests.commons import RequestType
from tests.error_messages import REQUIRED_FIELD_MSG


@pytest.mark.django_db
class TestGroupEndpoints:
    view_name_list = 'api:v1:group-list'
    view_name_detail = 'api:v1:group-detail'

    def test_list(self, api_client, authorized_superuser, group_factory):
        expected_instances = []
        for _ in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
            expected_instances.append(model_to_dict(group_factory()))

        response = api_client.send_request(self.view_name_list)
        for instance in json.loads(response.content):
            instance.pop('url')
            assert instance in expected_instances

    def test_retrieve(self, api_client, authorized_superuser, group):
        expected_dict = model_to_dict(group)
        response = api_client.send_request(self.view_name_detail, reverse_kwargs={'pk': group.pk})
        actual_dict = json.loads(response.content)
        actual_dict.pop('url')
        assert actual_dict == expected_dict

    def test_creation(self, api_client, authorized_superuser):
        expected_number_of_parameters = 1
        group_dict = {
            'name': constants.PARAMETER_GROUP_NAME,
            'permissions': []
        }
        api_client.send_request(self.view_name_list, group_dict, HTTPStatus.CREATED, RequestType.POST)
        assert Group.objects.count() == expected_number_of_parameters, f'Expected number of groups is ' \
                                                                       f'"{expected_number_of_parameters}"' \
                                                                       f'actual: "{Parameter.objects.count()}"'

    def test_partial_update(self, api_client, authorized_superuser, group):
        new_name = 'new_name'
        group_dict = {
            'id': group.id,
            'name': new_name,
        }
        api_client.send_request(
            self.view_name_detail,
            reverse_kwargs={'pk': group.pk},
            request_type=RequestType.PATCH,
            data=group_dict
        )
        actual_name = Group.objects.get(pk=group.id).name
        assert actual_name == new_name, f'New name does not match. Expected data "{new_name}", actual: "{actual_name}"'

    @pytest.mark.parametrize('expected_status', [HTTPStatus.OK, HTTPStatus.BAD_REQUEST])
    def test_update(self, api_client, authorized_superuser, group, expected_status):
        new_name = 'new_name'
        group_dict = {
            'id': group.id,
        }
        if expected_status == HTTPStatus.OK:
            group_dict['name'] = new_name
        response = api_client.send_request(
            self.view_name_detail,
            reverse_kwargs={'pk': group.pk},
            request_type=RequestType.PUT,
            expected_status=expected_status,
            data=group_dict
        )
        if expected_status == HTTPStatus.OK:
            actual_name = Group.objects.get(pk=group.id).name
            assert actual_name == new_name, f'Group names do not match. Expected name "{actual_name}", ' \
                                            f'actual: "{new_name}"'
        else:
            assert json.loads(response.content)['name'][0] == REQUIRED_FIELD_MSG

    def test_delete(self, api_client, authorized_superuser, group):
        assert Group.objects.count() == 1, 'Group was not created'
        api_client.send_request(
            self.view_name_detail,
            expected_status=HTTPStatus.NO_CONTENT,
            request_type=RequestType.DELETE,
            reverse_kwargs={'pk': group.pk}
        )
        assert not Group.objects.count(), f'Group with id "{group.id}" was not deleted.'
