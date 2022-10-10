import json
from http import HTTPStatus

import constants
import pytest
from factories import TestResultFactory, UserFactory
from tests_representation.choices import TestStatuses
from tests_representation.models import TestResult
from users.models import User


@pytest.mark.django_db
class TestResultView:

    def test_result_retrieve(self, api_client, authorized_superuser):
        number_of_results = 10
        expected_results_ids = []
        for _ in range(number_of_results):
            expected_results_ids.append(TestResultFactory.create().id)

        response = api_client.get(constants.RESULTS_URL)
        for result in json.loads(response.content):
            assert result.get('id') in expected_results_ids, f'Id "{result.get("id")}" was not in' \
                                                             'list of expected ids'
        assert response.status_code == HTTPStatus.OK, f'Expected response code "{HTTPStatus.OK}", ' \
                                                      f'actual: "{response.status_code}"'

    def test_result_creation(self, api_client, authorized_superuser, test, default_user):
        expected_number_of_results = 1
        result_json = {
            'status': TestStatuses.UNTESTED,
            'test': test.id,
            'user': default_user.id,
            'comment': constants.TEST_COMMENT,
        }
        response = api_client.post(constants.RESULTS_URL, data=result_json)
        assert response.status_code == HTTPStatus.CREATED, f'Expected response code "{HTTPStatus.CREATED}", ' \
                                                           f'actual: "{response.status_code}"'
        assert TestResult.objects.count() == expected_number_of_results, f'Expected number of users ' \
                                                                         f'"{expected_number_of_results}"' \
                                                                         f'actual: "{TestResult.objects.count()}"'

    def test_result_update(self, api_client, authorized_superuser, test_result, default_user):
        new_user = UserFactory.create()
        result_json = {
            'id': test_result.id,
            'user': new_user.id
        }
        response = api_client.patch(constants.SINGLE_RESULT_URL.format(id=test_result.id), data=result_json)
        assert response.status_code == HTTPStatus.OK, f'Expected response code "{HTTPStatus.OK}", ' \
                                                      f'actual: "{response.status_code}"'
        result_user = TestResult.objects.get(pk=test_result.id).user
        assert result_user == new_user, f'Result user does not match. Expected user "{new_user}", ' \
                                        f'actual: "{result_user}"'

    def test_result_delete(self, api_client, authorized_superuser, test_result):
        assert TestResult.objects.count() == 1
        response = api_client.delete(constants.SINGLE_RESULT_URL.format(id=test_result.id))
        assert response.status_code == HTTPStatus.NO_CONTENT, f'Expected response code "{HTTPStatus.NO_CONTENT}", ' \
                                                              f'actual: "{response.status_code}"'
        assert not User.objects.filter(pk=test_result.id), f'Result with id "{test_result.id}" was not deleted.'
