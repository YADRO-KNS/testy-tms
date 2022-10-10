import json
from http import HTTPStatus

import constants
import pytest
from factories import UserFactory
from users.models import User


@pytest.mark.django_db
class TestUserView:

    def test_user_retrieve(self, api_client, authorized_default_user, default_user):
        number_of_users = 10
        expected_users_names_list = [default_user.username]

        assert User.objects.count() == 1, 'Extra users were found, before adding more.'

        for _ in range(number_of_users):
            expected_users_names_list.append(UserFactory.create().username)

        response = api_client.get(constants.USERS_URL)
        for user in json.loads(response.content):
            assert user.get('username') in expected_users_names_list, f'Username "{user.get("username")}" was not in' \
                                                                      'list of expected usernames'
        assert response.status_code == HTTPStatus.OK, f'Expected response code "{HTTPStatus.OK}", ' \
                                                      f'actual: "{response.status_code}"'

    def test_user_creation(self, api_client, authorized_superuser):
        expected_users_num = 2
        assert User.objects.count() == 1, 'Extra users were found.'
        user_json = {
            'username': constants.USERNAME,
            'first_name': constants.FIRST_NAME,
            'last_name': constants.LAST_NAME,
            'password': constants.PASSWORD,
            'email': constants.USER_EMAIL
        }
        response = api_client.post(constants.USERS_URL, data=user_json)
        assert response.status_code == HTTPStatus.CREATED, f'Expected response code "{HTTPStatus.CREATED}", ' \
                                                           f'actual: "{response.status_code}"'
        assert User.objects.count() == expected_users_num, f'Expected number of users "{expected_users_num}"' \
                                                           f'actual: "{User.objects.count()}"'

    def test_user_update(self, api_client, authorized_superuser, default_user):
        user_id = default_user.id
        new_name = 'new_expected_username'
        user_json = {
            'id': user_id,
            'username': new_name,
            'password': default_user.password
        }
        response = api_client.patch(constants.SINGLE_USER_URL.format(id=user_id), data=user_json)
        assert response.status_code == HTTPStatus.OK, f'Expected response code "{HTTPStatus.OK}", ' \
                                                      f'actual: "{response.status_code}"'
        actual_name = User.objects.get(pk=user_id).username
        assert actual_name == new_name, f'Username does not match. Expected name "{actual_name}", actual: "{new_name}"'

    def test_user_delete(self, api_client, authorized_superuser, default_user):
        user_id = default_user.id
        response = api_client.delete(constants.SINGLE_USER_URL.format(id=user_id))
        assert response.status_code == HTTPStatus.NO_CONTENT, f'Expected response code "{HTTPStatus.NO_CONTENT}", ' \
                                                              f'actual: "{response.status_code}"'
        assert not User.objects.filter(pk=user_id), f'User with id "{user_id}" was not deleted.'
