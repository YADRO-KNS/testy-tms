import json
from http import HTTPStatus

import pytest
from django.forms import model_to_dict

from tests.error_messages import REQUIRED_FIELD_MSG
from tests_description.models import TestSuite

from tests import constants
from tests.commons import RequestType


@pytest.mark.django_db
class TestSuiteEndpoints:
    view_name_list = 'api:v1:testsuite-list'
    view_name_detail = 'api:v1:testsuite-detail'

    def test_list(self, api_client, authorized_superuser, test_suite_factory):
        expected_instances = []
        for _ in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
            expected_instances.append(model_to_dict(test_suite_factory()))

        response = api_client.send_request(self.view_name_list)
        for instance_dict in json.loads(response.content):
            instance_dict.pop('url')
            assert instance_dict in expected_instances, f'{instance_dict} was not found in expected instances.'

    def test_retrieve(self, api_client, authorized_superuser, test_suite):
        expected_dict = model_to_dict(test_suite)
        response = api_client.send_request(self.view_name_detail, reverse_kwargs={'pk': test_suite.pk})
        actual_dict = json.loads(response.content)
        actual_dict.pop('url')
        assert actual_dict == expected_dict, 'Actual model dict is different from expected'

    def test_creation(self, api_client, authorized_superuser, project):
        expected_number_of_suites = 1
        suite_dict = {
            'name': constants.TEST_CASE_NAME,
            'project': project.id,
        }
        api_client.send_request(self.view_name_list, suite_dict, HTTPStatus.CREATED, RequestType.POST)
        assert TestSuite.objects.count() == expected_number_of_suites, f'Expected number of users ' \
                                                                       f'"{expected_number_of_suites}"' \
                                                                       f'actual: "{TestSuite.objects.count()}"'

    def test_partial_update(self, api_client, authorized_superuser, test_suite):
        new_name = 'new_expected_test_case_name'
        suite_dict = {
            'id': test_suite.id,
            'name': new_name
        }
        api_client.send_request(
            self.view_name_detail,
            suite_dict,
            request_type=RequestType.PATCH,
            reverse_kwargs={'pk': test_suite.pk}
        )
        actual_name = TestSuite.objects.get(pk=test_suite.id).name
        assert actual_name == new_name, f'Suite names do not match. Expected name "{actual_name}", ' \
                                        f'actual: "{new_name}"'

    @pytest.mark.parametrize('expected_status', [HTTPStatus.OK, HTTPStatus.BAD_REQUEST])
    def test_update(self, api_client, authorized_superuser, expected_status, test_suite, project):
        new_name = 'new_expected_test_case_name'
        suite_dict = {
            'id': test_suite.id,
            'name': new_name
        }
        if expected_status == HTTPStatus.OK:
            suite_dict['project'] = project.id
        response = api_client.send_request(
            self.view_name_detail,
            reverse_kwargs={'pk': test_suite.pk},
            request_type=RequestType.PUT,
            expected_status=expected_status,
            data=suite_dict
        )
        if expected_status == HTTPStatus.OK:
            actual_name = TestSuite.objects.get(pk=test_suite.id).name
            assert actual_name == new_name, f'Suite name does not match. Expected name "{actual_name}", ' \
                                            f'actual: "{new_name}"'
        else:
            assert json.loads(response.content)['project'][0] == REQUIRED_FIELD_MSG

    def test_delete(self, api_client, authorized_superuser, test_suite):
        assert TestSuite.objects.count() == 1, 'Test suite was not created'
        api_client.send_request(
            self.view_name_detail,
            expected_status=HTTPStatus.NO_CONTENT,
            request_type=RequestType.DELETE,
            reverse_kwargs={'pk': test_suite.pk}
        )
        assert not TestSuite.objects.count(), f'Test suite with id "{test_suite.id}" was not deleted.'
