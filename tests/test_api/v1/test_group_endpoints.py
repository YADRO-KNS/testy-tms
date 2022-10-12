import json
from http import HTTPStatus

import pytest
from django.forms import model_to_dict
from tests_representation.models import Parameter
from users.models import Group

from tests import constants
from tests.commons import RequestType


@pytest.mark.django_db
class TestGroupEndpoints:

    def test_list(self, api_client, authorized_superuser, group_factory):
        expected_instances = []
        for _ in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
            expected_instances.append(model_to_dict(group_factory()))

        response = api_client.send_request('api:v1:group-list')
        for instance in json.loads(response.content):
            instance.pop('url')
            assert instance in expected_instances

    def test_retrieve(self, api_client, authorized_superuser, group):
        expected_dict = model_to_dict(group)
        response = api_client.send_request('api:v1:group-detail', reverse_kwargs={'pk': group.pk})
        actual_dict = json.loads(response.content)
        actual_dict.pop('url')
        assert actual_dict == expected_dict

    def test_creation(self, api_client, authorized_superuser):
        expected_number_of_parameters = 1
        group_json = {
            'name': constants.PARAMETER_GROUP_NAME,
            'permissions': []
        }
        api_client.send_request('api:v1:group-list', group_json, HTTPStatus.CREATED, RequestType.POST)
        assert Group.objects.count() == expected_number_of_parameters, f'Expected number of groups is ' \
                                                                       f'"{expected_number_of_parameters}"' \
                                                                       f'actual: "{Parameter.objects.count()}"'

    def test_partial_update(self, api_client, authorized_superuser, group):
        new_name = 'new_name'
        group_json = {
            'id': group.id,
            'name': new_name,
        }
        api_client.send_request(
            'api:v1:group-detail',
            reverse_kwargs={'pk': group.pk},
            request_type=RequestType.PATCH,
            data=group_json
        )
        actual_name = Group.objects.get(pk=group.id).name
        assert actual_name == new_name, f'New name does not match. Expected data "{new_name}", actual: "{actual_name}"'

    def test_delete(self, api_client, authorized_superuser, group):
        assert Group.objects.count() == 1, 'Group was not created'
        api_client.send_request(
            'api:v1:group-detail',
            expected_status=HTTPStatus.NO_CONTENT,
            request_type=RequestType.DELETE,
            reverse_kwargs={'pk': group.pk}
        )
        assert not Group.objects.count(), f'Group with id "{group.id}" was not deleted.'
