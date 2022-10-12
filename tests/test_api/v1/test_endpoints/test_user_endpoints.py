import json
from http import HTTPStatus
from typing import Any, Dict

import pytest
from django.forms import model_to_dict
from users.models import User

from tests import constants
from tests.commons import RequestType


@pytest.mark.django_db
class TestUserEndpoints:

    def test_list(self, api_client, authorized_superuser, user_factory):
        expected_instances = [self._form_dict_user_model(authorized_superuser)]
        for _ in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
            expected_instances.append(self._form_dict_user_model(user_factory()))
        response = api_client.send_request('api:v1:user-list')

        for instance_dict in json.loads(response.content):
            instance_dict.pop('url')
            assert instance_dict in expected_instances, f'{instance_dict} was not found in expected instances.'

    def test_retrieve(self, api_client, authorized_superuser, user):
        expected_dict = self._form_dict_user_model(user)
        response = api_client.send_request('api:v1:user-detail', reverse_kwargs={'pk': user.pk})
        actual_dict = json.loads(response.content)
        actual_dict.pop('url')
        assert actual_dict == expected_dict, 'Actual model dict is different from expected'

    def test_creation(self, api_client, authorized_superuser):
        expected_users_num = 2
        assert User.objects.count() == 1, 'Extra users were found.'
        user_json = {
            'username': constants.USERNAME,
            'first_name': constants.FIRST_NAME,
            'last_name': constants.LAST_NAME,
            'password': constants.PASSWORD,
            'email': constants.USER_EMAIL
        }
        api_client.send_request('api:v1:user-list', user_json, HTTPStatus.CREATED, RequestType.POST)
        assert User.objects.count() == expected_users_num, f'Expected number of users "{expected_users_num}"' \
                                                           f'actual: "{User.objects.count()}"'

    def test_partial_update(self, api_client, authorized_superuser, user):
        new_name = 'new_expected_username'
        user_json = {
            'id': user.id,
            'username': new_name,
            'password': user.password
        }
        api_client.send_request(
            'api:v1:user-detail',
            user_json,
            request_type=RequestType.PATCH,
            reverse_kwargs={'pk': user.pk}
        )
        actual_name = User.objects.get(pk=user.id).username
        assert actual_name == new_name, f'Username does not match. Expected name "{actual_name}", actual: "{new_name}"'

    def test_delete(self, api_client, authorized_superuser, user):
        assert User.objects.count() == 2, 'User was not created'
        api_client.send_request(
            'api:v1:user-detail',
            expected_status=HTTPStatus.NO_CONTENT,
            request_type=RequestType.DELETE,
            reverse_kwargs={'pk': user.pk}
        )
        assert User.objects.count() == 1, f'User with id "{user.id}" was not deleted.'

    @staticmethod
    def _form_dict_user_model(user: User) -> Dict[str, Any]:
        user_dict = model_to_dict(user)
        fields_to_remove = ['is_superuser', 'last_login', 'password', 'user_permissions']
        for field in fields_to_remove:
            user_dict.pop(field)
        user_dict['date_joined'] = user_dict['date_joined'].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return user_dict
