
import json
from http import HTTPStatus
from typing import Any, Dict

import pytest
from django.forms import model_to_dict
from users.models import User

from tests import constants
from tests.commons import RequestType
from tests.error_messages import INVALID_EMAIL_MSG, REQUIRED_FIELD_MSG, UNAUTHORIZED_MSG


@pytest.mark.django_db
class TestUserEndpoints:
    view_name_list = 'api:v1:user-list'
    view_name_detail = 'api:v1:user-detail'

    def test_list(self, api_client, authorized_superuser, user_factory):
        expected_instances = [self._form_dict_user_model(authorized_superuser)]
        for _ in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
            expected_instances.append(self._form_dict_user_model(user_factory()))
        response = api_client.send_request(self.view_name_list)

        for instance_dict in json.loads(response.content):
            instance_dict.pop('url')
            assert instance_dict in expected_instances, f'{instance_dict} was not found in expected instances.'

    def test_retrieve(self, api_client, authorized_superuser, user):
        expected_dict = self._form_dict_user_model(user)
        response = api_client.send_request(self.view_name_detail, reverse_kwargs={'pk': user.pk})
        actual_dict = json.loads(response.content)
        actual_dict.pop('url')
        assert actual_dict == expected_dict, 'Actual model dict is different from expected'

    def test_creation(self, api_client, authorized_superuser):
        expected_users_num = 2
        assert User.objects.count() == 1, 'Extra users were found.'
        user_dict = {
            'username': constants.USERNAME,
            'first_name': constants.FIRST_NAME,
            'last_name': constants.LAST_NAME,
            'password': constants.PASSWORD,
            'email': constants.USER_EMAIL
        }
        api_client.send_request(self.view_name_list, user_dict, HTTPStatus.CREATED, RequestType.POST)
        assert User.objects.count() == expected_users_num, f'Expected number of users "{expected_users_num}"' \
                                                           f'actual: "{User.objects.count()}"'

    def test_partial_update(self, api_client, authorized_superuser, user):
        new_name = 'new_expected_username'
        user_dict = {
            'id': user.id,
            'username': new_name,
        }
        api_client.send_request(
            self.view_name_detail,
            user_dict,
            request_type=RequestType.PATCH,
            reverse_kwargs={'pk': user.pk}
        )
        actual_name = User.objects.get(pk=user.id).username
        assert actual_name == new_name, f'Username does not match. Expected name "{actual_name}", actual: "{new_name}"'

    @pytest.mark.parametrize('expected_status', [HTTPStatus.OK, HTTPStatus.BAD_REQUEST])
    def test_update(self, api_client, authorized_superuser, user, expected_status):
        new_name = 'new_expected_username'
        user_dict = {
            'id': user.id,
            'username': new_name,
        }
        if expected_status == HTTPStatus.OK:
            user_dict['password'] = user.password
        response = api_client.send_request(
            self.view_name_detail,
            user_dict,
            request_type=RequestType.PUT,
            expected_status=expected_status,
            reverse_kwargs={'pk': user.pk}
        )
        if expected_status == HTTPStatus.OK:
            actual_name = User.objects.get(pk=user.id).username
            assert actual_name == new_name, f'Username does not match. Expected name "{actual_name}", ' \
                                            f'actual: "{new_name}"'
        else:
            assert json.loads(response.content)['password'][0] == REQUIRED_FIELD_MSG

    def test_delete(self, api_client, authorized_superuser, user):
        assert User.objects.count() == 2, 'User was not created'
        api_client.send_request(
            self.view_name_detail,
            expected_status=HTTPStatus.NO_CONTENT,
            request_type=RequestType.DELETE,
            reverse_kwargs={'pk': user.pk}
        )
        assert User.objects.count() == 1, f'User with id "{user.id}" was not deleted.'

    def test_unauthorized_access(self, api_client):
        for request_type in RequestType:
            response = api_client.send_request(
                self.view_name_list,
                expected_status=HTTPStatus.UNAUTHORIZED,
                request_type=request_type
            )
            received_dict = json.loads(response.content)
            assert received_dict['detail'] == UNAUTHORIZED_MSG, 'Expected message was not found in response.' \
                                                                f'Request type: {RequestType.POST.value}'

    def test_email_validation(self, api_client, authorized_superuser, user):
        update_types = [RequestType.PUT, RequestType.PATCH]
        user_dict = {
            'username': constants.USERNAME,
            'password': constants.PASSWORD,
            'email': constants.INVALID_EMAIL
        }
        response = api_client.send_request(self.view_name_list, user_dict, HTTPStatus.BAD_REQUEST, RequestType.POST)
        received_dict = json.loads(response.content)
        assert received_dict['email'][0] == INVALID_EMAIL_MSG, 'Validation email error was not found in response.' \
                                                               f'Request type: {RequestType.POST.value}'
        user_dict_update = {
            'username': constants.USERNAME,
            'password': constants.PASSWORD,
            'email': constants.INVALID_EMAIL
        }
        for request_type in update_types:
            response = api_client.send_request(
                self.view_name_detail,
                data=user_dict_update,
                expected_status=HTTPStatus.BAD_REQUEST,
                request_type=request_type,
                reverse_kwargs={'pk': user.pk}
            )
            received_dict = json.loads(response.content)
            assert received_dict['email'][0] == INVALID_EMAIL_MSG, 'Validation email error was not found in response.' \
                                                                   f'Request type: {request_type.value}'

    @staticmethod
    def _form_dict_user_model(user: User) -> Dict[str, Any]:
        user_dict = model_to_dict(user)
        fields_to_remove = ['is_superuser', 'last_login', 'password', 'user_permissions']
        for field in fields_to_remove:
            user_dict.pop(field)
        user_dict['date_joined'] = user_dict['date_joined'].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return user_dict
