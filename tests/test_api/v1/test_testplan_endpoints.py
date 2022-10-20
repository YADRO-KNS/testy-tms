import json
from http import HTTPStatus

import pytest
from django.forms import model_to_dict

from tests import constants
from tests.commons import RequestType
from tests.error_messages import REQUIRED_FIELD_MSG
from tests_representation.models import TestPlan


@pytest.mark.django_db
class TestPlanEndpoints:
    view_name_detail = 'api:v1:testplan-detail'
    view_name_list = 'api:v1:testplan-list'

    @pytest.mark.parametrize('number_of_instances', [constants.NUMBER_OF_OBJECTS_TO_CREATE])
    def test_list(self, api_client, authorized_superuser, several_test_plans_by_api):
        expected_instances = several_test_plans_by_api
        response = api_client.send_request(self.view_name_list)

        for instance_dict in json.loads(response.content):
            assert instance_dict in expected_instances, f'{instance_dict} was not found in expected instances.'

    def test_retrieve(self, api_client, authorized_superuser, test_plan_by_api):
        response = api_client.send_request(self.view_name_detail, reverse_kwargs={'pk': test_plan_by_api.get('id')})
        actual_dict = json.loads(response.content)
        assert actual_dict == test_plan_by_api, 'Actual model dict is different from expected'

    @pytest.mark.parametrize('number_of_param_groups, number_of_entities_in_group', [(1, 3), (2, 2), (3, 4)])
    def test_creation(self, api_client, authorized_superuser, combined_parameters):
        parameters, expected_number_of_plans = combined_parameters
        testplan_dict = {
            "name": f"Test plan",
            "due_date": constants.DATE.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "started_at": constants.DATE.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "parameters": parameters
        }
        response = api_client.send_request(self.view_name_list, testplan_dict, HTTPStatus.CREATED, RequestType.POST)
        endpoint_plans = json.loads(response.content)
        assert TestPlan.objects.count() == expected_number_of_plans, f'Expected number of test plans ' \
                                                                     f'"{expected_number_of_plans}"' \
                                                                     f'actual: "{TestPlan.objects.count()}"'
        assert len(endpoint_plans) == expected_number_of_plans, f'Expected number of test plans from endpoint ' \
                                                                f'"{expected_number_of_plans}"' \
                                                                f'actual: "{len(endpoint_plans)}"'

    def test_partial_update(self, api_client, authorized_superuser, test_case):
        new_name = 'new_expected_test_case_name'
        case_dict = {
            'id': test_case.id,
            'name': new_name
        }
        api_client.send_request(
            self.view_name_detail,
            case_dict,
            request_type=RequestType.PATCH,
            reverse_kwargs={'pk': test_case.pk}
        )
        actual_name = TestCase.objects.get(pk=test_case.id).name
        assert actual_name == new_name, f'Names do not match. Expected name "{actual_name}", actual: "{new_name}"'

    @pytest.mark.parametrize('expected_status', [HTTPStatus.OK, HTTPStatus.BAD_REQUEST])
    def test_update(self, api_client, authorized_superuser, expected_status, test_case, project, test_suite):
        new_name = 'new_expected_test_case_name'
        case_dict = {
            'id': test_case.id,
            'name': new_name
        }
        if expected_status == HTTPStatus.OK:
            case_dict['project'] = project.id
            case_dict['suite'] = test_suite.id
            case_dict['scenario'] = constants.SCENARIO
        response = api_client.send_request(
            self.view_name_detail,
            reverse_kwargs={'pk': test_case.pk},
            request_type=RequestType.PUT,
            expected_status=expected_status,
            data=case_dict
        )
        if expected_status == HTTPStatus.OK:
            actual_name = TestCase.objects.get(pk=test_case.id).name
            assert actual_name == new_name, f'Username does not match. Expected name "{actual_name}", ' \
                                            f'actual: "{new_name}"'
        else:
            assert json.loads(response.content)['project'][0] == REQUIRED_FIELD_MSG
            assert json.loads(response.content)['suite'][0] == REQUIRED_FIELD_MSG
            assert json.loads(response.content)['scenario'][0] == REQUIRED_FIELD_MSG

    def test_delete(self, api_client, authorized_superuser, test_case):
        assert TestCase.objects.count() == 1, 'Test case was not created'
        api_client.send_request(
            self.view_name_detail,
            expected_status=HTTPStatus.NO_CONTENT,
            request_type=RequestType.DELETE,
            reverse_kwargs={'pk': test_case.pk}
        )
        assert not TestCase.objects.count(), f'TestCase with id "{test_case.id}" was not deleted.'


test_plan = {
    "name": "Test plan",
    "due_date": "2012-04-23T18:25:43.511Z",
    "started_at": "2012-04-23T18:25:43.511Z",
    "parameters": [1, 2, 3]
}
update = {"tests": [1, 2, 3]}
