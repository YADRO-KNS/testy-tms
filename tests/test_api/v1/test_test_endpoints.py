
import json
from http import HTTPStatus

import pytest
from tests_representation.models import Test

from tests import constants
from tests.commons import RequestType, model_with_base_to_dict
from tests.error_messages import REQUIRED_FIELD_MSG


@pytest.mark.django_db
class TestTestEndpoints:
    view_name_list = 'api:v1:test-list'
    view_name_detail = 'api:v1:test-detail'

    def test_list(self, api_client, authorized_superuser, test_factory):
        expected_instances = []
        for _ in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
            expected_instances.append(model_with_base_to_dict(test_factory()))

        response = api_client.send_request(self.view_name_list)
        for instance_dict in json.loads(response.content):
            instance_dict.pop('url')
            assert instance_dict in expected_instances, f'{instance_dict} was not found in expected instances.'

    def test_retrieve(self, api_client, authorized_superuser, test):
        expected_dict = model_with_base_to_dict(test)
        response = api_client.send_request(self.view_name_detail, reverse_kwargs={'pk': test.pk})
        actual_dict = json.loads(response.content)
        actual_dict.pop('url')
        assert actual_dict == expected_dict, 'Actual model dict is different from expected'

    def test_partial_update(self, api_client, authorized_superuser, test, user):
        result_dict = {
            'id': test.id,
            'user': user.id
        }
        api_client.send_request(
            self.view_name_detail,
            result_dict,
            request_type=RequestType.PATCH,
            reverse_kwargs={'pk': test.pk}
        )
        result_user = Test.objects.get(pk=test.id).user
        assert result_user == user, f'Test user does not match. Expected user "{user}", ' \
                                    f'actual: "{result_user}"'

    @pytest.mark.parametrize('expected_status', [HTTPStatus.OK, HTTPStatus.BAD_REQUEST])
    def test_update(self, api_client, authorized_superuser, expected_status, test, user, test_case, test_plan):
        result_dict = {
            'id': test.id,
            'user': user.id
        }
        if expected_status == HTTPStatus.OK:
            result_dict['case'] = test_case.id
            result_dict['plan'] = test_plan.id

        response = api_client.send_request(
            self.view_name_detail,
            reverse_kwargs={'pk': test.pk},
            request_type=RequestType.PUT,
            expected_status=expected_status,
            data=result_dict
        )
        if expected_status == HTTPStatus.OK:
            result_user = Test.objects.get(pk=test.id).user
            assert result_user == user, f'Test user does not match. Expected user "{user}", ' \
                                        f'actual: "{result_user}"'
        else:
            assert json.loads(response.content)['case'][0] == REQUIRED_FIELD_MSG
            assert json.loads(response.content)['plan'][0] == REQUIRED_FIELD_MSG

    def test_test_cannot_be_deleted(self, api_client, authorized_superuser, test):
        assert Test.objects.count() == 1, 'Test was not created'
        api_client.send_request(
            self.view_name_detail,
            expected_status=HTTPStatus.METHOD_NOT_ALLOWED,
            request_type=RequestType.DELETE,
            reverse_kwargs={'pk': test.pk}
        )
        assert Test.objects.count(), f'Test with id "{test.id}" was not deleted.'
