import json
from http import HTTPStatus

import constants
import pytest
from factories import TestFactory, UserFactory
from tests_representation.models import Test


# TODO: currently not working
@pytest.mark.django_db
class TestTestView:

    def test_test_retrieve(self, api_client, authorized_superuser):
        number_of_tests = 10
        expected_tests_id = []
        for _ in range(number_of_tests):
            expected_tests_id.append(TestFactory.create().id)

        response = api_client.get(constants.TESTS_URL)
        for test in json.loads(response.content):
            assert test.get('id') in expected_tests_id, f'Name "{test.get("id")}" was not in' \
                                                        'list of expected names'
        assert response.status_code == HTTPStatus.OK, f'Expected response code "{HTTPStatus.OK}", ' \
                                                      f'actual: "{response.status_code}"'

    def test_test_creation(self, api_client, authorized_superuser, test_case, test_plan, default_user):
        expected_number_of_tests = 1
        test_json = {
            'case': test_case.id,
            'plan': test_plan.id,
            'user': default_user.id,
        }
        response = api_client.post(constants.TESTS_URL, data=test_json)
        assert response.status_code == HTTPStatus.CREATED, f'Expected response code "{HTTPStatus.CREATED}", ' \
                                                           f'actual: "{response.status_code}"'
        assert Test.objects.count() == expected_number_of_tests, f'Expected number of users ' \
                                                                 f'"{expected_number_of_tests}"' \
                                                                 f'actual: "{Test.objects.count()}"'

    def test_test_update(self, api_client, authorized_superuser, test, default_user):
        new_user = UserFactory.create()
        result_json = {
            'id': test.id,
            'user': new_user.id
        }
        response = api_client.patch(constants.SINGLE_TEST_URL.format(id=test.id), data=result_json)
        assert response.status_code == HTTPStatus.OK, f'Expected response code "{HTTPStatus.OK}", ' \
                                                      f'actual: "{response.status_code}"'
        result_user = Test.objects.get(pk=test.id).user
        assert result_user == new_user, f'Test user does not match. Expected user "{new_user}", ' \
                                        f'actual: "{result_user}"'

    def test_test_delete(self, api_client, authorized_superuser, test):
        assert Test.objects.count() == 1
        response = api_client.delete(constants.SINGLE_TEST_URL.format(id=test.id))
        assert response.status_code == HTTPStatus.NO_CONTENT, f'Expected response code "{HTTPStatus.NO_CONTENT}", ' \
                                                              f'actual: "{response.status_code}"'
        assert not Test.objects.filter(pk=test.id), f'Test with id "{test.id}" was not deleted.'
