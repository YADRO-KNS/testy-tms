import json
from http import HTTPStatus

import constants
import pytest
from factories import TestCaseFactory
from tests_description.models import TestCase
from users.models import User


@pytest.mark.django_db
class TestCaseView:

    def test_case_retrieve(self, api_client, authorized_superuser):
        number_of_users = 10
        expected_cases_names_list = []
        for _ in range(number_of_users):
            expected_cases_names_list.append(TestCaseFactory.create().name)

        response = api_client.get(constants.CASES_URL)
        for case in json.loads(response.content):
            assert case.get('name') in expected_cases_names_list, f'Name "{case.get("name")}" was not in' \
                                                                  'list of expected names'
        assert response.status_code == HTTPStatus.OK, f'Expected response code "{HTTPStatus.OK}", ' \
                                                      f'actual: "{response.status_code}"'

    def test_case_creation(self, api_client, authorized_superuser, project, test_suite):
        expected_number_of_cases = 1
        case_json = {
            'name': constants.TEST_CASE_NAME,
            'project': project.id,
            'suite': test_suite.id,
            'setup': constants.SETUP,
            'scenario': constants.SCENARIO,
            'teardown': constants.TEARDOWN,
            'estimate': constants.ESTIMATE
        }
        response = api_client.post(constants.CASES_URL, data=case_json)
        assert response.status_code == HTTPStatus.CREATED, f'Expected response code "{HTTPStatus.CREATED}", ' \
                                                           f'actual: "{response.status_code}"'
        assert TestCase.objects.count() == expected_number_of_cases, f'Expected number of users ' \
                                                                     f'"{expected_number_of_cases}"' \
                                                                     f'actual: "{TestCase.objects.count()}"'

    def test_case_update(self, api_client, authorized_superuser, test_case):
        new_name = 'new_expected_test_case_name'
        case_json = {
            'id': test_case.id,
            'name': new_name
        }
        response = api_client.patch(constants.SINGLE_CASE_URL.format(id=test_case.id), data=case_json)
        assert response.status_code == HTTPStatus.OK, f'Expected response code "{HTTPStatus.OK}", ' \
                                                      f'actual: "{response.status_code}"'
        actual_name = TestCase.objects.get(pk=test_case.id).name
        assert actual_name == new_name, f'Username does not match. Expected name "{actual_name}", actual: "{new_name}"'

    def test_user_delete(self, api_client, authorized_superuser, test_case):
        assert TestCase.objects.count() == 1
        response = api_client.delete(constants.SINGLE_CASE_URL.format(id=test_case.id))
        assert response.status_code == HTTPStatus.NO_CONTENT, f'Expected response code "{HTTPStatus.NO_CONTENT}", ' \
                                                              f'actual: "{response.status_code}"'
        assert not User.objects.filter(pk=test_case.id), f'Case with id "{test_case.id}" was not deleted.'
