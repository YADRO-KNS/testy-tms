import json
from http import HTTPStatus

import pytest
from django.forms import model_to_dict

from tests.error_messages import REQUIRED_FIELD_MSG
from tests_representation.models import Parameter
from users.models import Group

from tests import constants
from tests.commons import RequestType


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
