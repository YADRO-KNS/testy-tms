import json
from http import HTTPStatus

import constants
import pytest
from factories import TestSuiteFactory
from tests_description.models import TestSuite
from users.models import User


@pytest.mark.django_db
class TestSuiteView:

    def test_suite_retrieve(self, api_client, authorized_superuser):
        number_of_suites = 10
        expected_suites_names_list = []
        for _ in range(number_of_suites):
            expected_suites_names_list.append(TestSuiteFactory.create().name)

        response = api_client.get(constants.SUITES_URL)
        for suite in json.loads(response.content):
            assert suite.get('name') in expected_suites_names_list, f'Name "{suite.get("name")}" was not in' \
                                                                    'list of expected names'
        assert response.status_code == HTTPStatus.OK, f'Expected response code "{HTTPStatus.OK}", ' \
                                                      f'actual: "{response.status_code}"'

    def test_suite_creation(self, api_client, authorized_superuser, project):
        expected_number_of_suites = 1
        suite_json = {
            'name': constants.TEST_CASE_NAME,
            'project': project.id,
        }
        response = api_client.post(constants.SUITES_URL, data=suite_json)
        assert response.status_code == HTTPStatus.CREATED, f'Expected response code "{HTTPStatus.CREATED}", ' \
                                                           f'actual: "{response.status_code}"'
        assert TestSuite.objects.count() == expected_number_of_suites, f'Expected number of users ' \
                                                                       f'"{expected_number_of_suites}"' \
                                                                       f'actual: "{TestSuite.objects.count()}"'

    def test_suite_update(self, api_client, authorized_superuser, test_suite):
        new_name = 'new_expected_test_case_name'
        suite_json = {
            'id': test_suite.id,
            'name': new_name
        }
        response = api_client.patch(constants.SINGLE_SUITE_URL.format(id=test_suite.id), data=suite_json)
        assert response.status_code == HTTPStatus.OK, f'Expected response code "{HTTPStatus.OK}", ' \
                                                      f'actual: "{response.status_code}"'
        actual_name = TestSuite.objects.get(pk=test_suite.id).name
        assert actual_name == new_name, f'Suite name does not match. Expected name "{actual_name}", ' \
                                        f'actual: "{new_name}"'

    def test_suite_delete(self, api_client, authorized_superuser, test_suite):
        assert TestSuite.objects.count() == 1
        response = api_client.delete(constants.SINGLE_SUITE_URL.format(id=test_suite.id))
        assert response.status_code == HTTPStatus.NO_CONTENT, f'Expected response code "{HTTPStatus.NO_CONTENT}", ' \
                                                              f'actual: "{response.status_code}"'
        assert not User.objects.filter(pk=test_suite.id), f'Suite with id "{test_suite.id}" was not deleted.'
