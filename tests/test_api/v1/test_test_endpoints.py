import json
from http import HTTPStatus

import pytest
from tests_representation.models import Test

from tests import constants
from tests.commons import RequestType, model_with_base_to_dict


@pytest.mark.django_db
class TestTestEndpoints:

    def test_list(self, api_client, authorized_superuser, test_factory):
        expected_instances = []
        for _ in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
            expected_instances.append(model_with_base_to_dict(test_factory()))

        response = api_client.send_request('api:v1:test-list')
        for instance_dict in json.loads(response.content):
            instance_dict.pop('url')
            assert instance_dict in expected_instances, f'{instance_dict} was not found in expected instances.'

    def test_retrieve(self, api_client, authorized_superuser, test):
        expected_dict = model_with_base_to_dict(test)
        response = api_client.send_request('api:v1:test-detail', reverse_kwargs={'pk': test.pk})
        actual_dict = json.loads(response.content)
        actual_dict.pop('url')
        assert actual_dict == expected_dict, 'Actual model dict is different from expected'

    def test_partial_update(self, api_client, authorized_superuser, test, user):
        result_dict = {
            'id': test.id,
            'user': user.id
        }
        api_client.send_request(
            'api:v1:test-detail',
            result_dict,
            request_type=RequestType.PATCH,
            reverse_kwargs={'pk': test.pk}
        )
        result_user = Test.objects.get(pk=test.id).user
        assert result_user == user, f'Test user does not match. Expected user "{user}", ' \
                                    f'actual: "{result_user}"'

    def test_test_cannot_be_deleted(self, api_client, authorized_superuser, test):
        assert Test.objects.count() == 1, 'Test was not created'
        api_client.send_request(
            'api:v1:test-detail',
            expected_status=HTTPStatus.METHOD_NOT_ALLOWED,
            request_type=RequestType.DELETE,
            reverse_kwargs={'pk': test.pk}
        )
        assert Test.objects.count(), f'Test with id "{test.id}" was not deleted.'
