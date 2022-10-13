import json
from http import HTTPStatus

import pytest
from django.forms import model_to_dict
from tests_description.models import TestCase

from tests import constants
from tests.commons import RequestType


@pytest.mark.django_db
class TestCaseEndpoints:

    def test_list(self, api_client, authorized_superuser, test_case_factory):
        expected_instances = []
        for _ in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
            expected_instances.append(model_to_dict(test_case_factory()))

        response = api_client.send_request('api:v1:testcase-list')

        for instance_dict in json.loads(response.content):
            instance_dict.pop('url')
            assert instance_dict in expected_instances, f'{instance_dict} was not found in expected instances.'

    def test_retrieve(self, api_client, authorized_superuser, test_case):
        expected_dict = model_to_dict(test_case)
        response = api_client.send_request('api:v1:testcase-detail', reverse_kwargs={'pk': test_case.pk})
        actual_dict = json.loads(response.content)
        actual_dict.pop('url')
        assert actual_dict == expected_dict, 'Actual model dict is different from expected'

    def test_creation(self, api_client, authorized_superuser, project, test_suite):
        expected_number_of_cases = 1
        case_dict = {
            'name': constants.TEST_CASE_NAME,
            'project': project.id,
            'suite': test_suite.id,
            'setup': constants.SETUP,
            'scenario': constants.SCENARIO,
            'teardown': constants.TEARDOWN,
            'estimate': constants.ESTIMATE
        }
        api_client.send_request('api:v1:testcase-list', case_dict, HTTPStatus.CREATED, RequestType.POST)
        assert TestCase.objects.count() == expected_number_of_cases, f'Expected number of users ' \
                                                                     f'"{expected_number_of_cases}"' \
                                                                     f'actual: "{TestCase.objects.count()}"'

    def test_partial_update(self, api_client, authorized_superuser, test_case):
        new_name = 'new_expected_test_case_name'
        case_dict = {
            'id': test_case.id,
            'name': new_name
        }
        api_client.send_request(
            'api:v1:testcase-detail',
            case_dict,
            request_type=RequestType.PATCH,
            reverse_kwargs={'pk': test_case.pk}
        )
        actual_name = TestCase.objects.get(pk=test_case.id).name
        assert actual_name == new_name, f'Username does not match. Expected name "{actual_name}", actual: "{new_name}"'

    def test_delete(self, api_client, authorized_superuser, test_case):
        assert TestCase.objects.count() == 1, 'Test case was not created'
        api_client.send_request(
            'api:v1:testcase-detail',
            expected_status=HTTPStatus.NO_CONTENT,
            request_type=RequestType.DELETE,
            reverse_kwargs={'pk': test_case.pk}
        )
        assert not TestCase.objects.count(), f'TestCase with id "{test_case.id}" was not deleted.'
