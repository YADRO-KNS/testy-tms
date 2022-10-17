import json
from http import HTTPStatus

import pytest
from tests_representation.choices import TestStatuses
from tests_representation.models import TestResult

from tests import constants
from tests.commons import RequestType, model_with_base_to_dict
from tests.error_messages import REQUIRED_FIELD_MSG


@pytest.mark.django_db(reset_sequences=True)
class TestResultEndpoints:
    view_name_list = 'api:v1:testresult-list'
    view_name_detail = 'api:v1:testresult-detail'

    def test_list(self, api_client, authorized_superuser, test_result_factory):
        expected_instances = []
        for _ in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
            model_dict = model_with_base_to_dict(test_result_factory())
            model_dict['status'] = model_dict['status'].value
            expected_instances.append(model_dict)

        response = api_client.send_request(self.view_name_list)

        for instance_dict in json.loads(response.content):
            instance_dict.pop('url')
            assert instance_dict in expected_instances, f'{instance_dict} was not found in expected instances.'

    def test_retrieve(self, api_client, authorized_superuser, test_result):
        expected_dict = model_with_base_to_dict(test_result)
        expected_dict['status'] = expected_dict['status'].value
        response = api_client.send_request(self.view_name_detail, reverse_kwargs={'pk': test_result.pk})
        actual_dict = json.loads(response.content)
        actual_dict.pop('url')
        assert actual_dict == expected_dict, 'Actual model dict is different from expected'

    def test_creation(self, api_client, authorized_superuser, test, user):
        expected_number_of_results = 1
        result_dict = {
            'status': TestStatuses.UNTESTED,
            'test': test.id,
            'user': user.id,
            'comment': constants.TEST_COMMENT,
        }
        api_client.send_request(self.view_name_list, result_dict, HTTPStatus.CREATED, RequestType.POST)
        assert TestResult.objects.count() == expected_number_of_results, f'Expected number of users ' \
                                                                         f'"{expected_number_of_results}"' \
                                                                         f'actual: "{TestResult.objects.count()}"'

    def test_partial_update(self, api_client, authorized_superuser, test_result, user):
        result_dict = {
            'id': test_result.id,
            'user': user.id
        }
        api_client.send_request(
            self.view_name_detail,
            result_dict,
            request_type=RequestType.PATCH,
            reverse_kwargs={'pk': test_result.pk}
        )
        result_user = TestResult.objects.get(pk=test_result.id).user
        assert result_user == user, f'Result users do not match. Expected user "{user}", ' \
                                    f'actual: "{result_user}"'

    @pytest.mark.parametrize('expected_status', [HTTPStatus.OK, HTTPStatus.BAD_REQUEST])
    def test_update(self, api_client, authorized_superuser, expected_status, test_result, user, test):
        result_dict = {
            'id': test_result.id,
            'user': user.id
        }
        if expected_status == HTTPStatus.OK:
            result_dict['test'] = test.id
        response = api_client.send_request(
            self.view_name_detail,
            reverse_kwargs={'pk': test_result.pk},
            request_type=RequestType.PUT,
            expected_status=expected_status,
            data=result_dict
        )
        if expected_status == HTTPStatus.OK:
            result_user = TestResult.objects.get(pk=test_result.id).user
            assert result_user == user, f'Result users do not match. Expected user "{user}", actual: "{result_user}"'
        else:
            assert json.loads(response.content)['test'][0] == REQUIRED_FIELD_MSG

    def test_delete(self, api_client, authorized_superuser, test_result):
        assert TestResult.objects.count() == 1, 'Test result was not created'
        api_client.send_request(
            self.view_name_detail,
            expected_status=HTTPStatus.NO_CONTENT,
            request_type=RequestType.DELETE,
            reverse_kwargs={'pk': test_result.pk}
        )
        assert not TestResult.objects.count(), f'Test result with id "{test_result.id}" was not deleted.'

    def test_add_results_to_test(self, api_client, authorized_superuser, user, test_factory):
        tests = [test_factory(), test_factory()]
        for test in tests:
            result_dict = {
                'status': TestStatuses.UNTESTED,
                'test': test.id,
                'user': user.id,
                'comment': constants.TEST_COMMENT,
            }
            api_client.send_request(
                'api:v1:result-add',
                expected_status=HTTPStatus.CREATED,
                request_type=RequestType.POST,
                data=result_dict,
                reverse_kwargs={'test_id': test.id}
            )
        assert TestResult.objects.count() == 2, 'Expected number of results was not created.'
        assert TestResult.objects.filter(test=tests[0]).count() == 1, f'Only 1 result should be on a test "{tests[0]}"'
        assert TestResult.objects.filter(test=tests[1]).count() == 1, f'Only 1 result should be on a test "{tests[1]}"'

    def test_get_results_by_test(self, api_client, test_result_factory, test_factory, authorized_superuser):
        test1 = test_factory()
        test2 = test_factory()
        dicts_test1 = []
        dicts_test2 = []
        for _ in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
            dicts_test1.append(model_with_base_to_dict(test_result_factory(test=test1)))
            dicts_test2.append(model_with_base_to_dict(test_result_factory(test=test2)))
        response_test1 = api_client.send_request(
            'api:v1:results-by-test',
            expected_status=HTTPStatus.OK,
            request_type=RequestType.GET,
            reverse_kwargs={'test_id': test1.id}
        )
        response_test2 = api_client.send_request(
            'api:v1:results-by-test',
            expected_status=HTTPStatus.OK,
            request_type=RequestType.GET,
            reverse_kwargs={'test_id': test2.id}
        )
        actual_results1 = json.loads(response_test1.content)
        actual_results2 = json.loads(response_test2.content)
        for result_test1, result_test2 in zip(actual_results1, actual_results2):
            result_test1.pop('url')
            result_test2.pop('url')
        assert actual_results1 == dicts_test1, 'Response is different from expected one'
        assert actual_results2 == dicts_test2, 'Response is different from expected one'
