import copy
import json
from http import HTTPStatus

import pytest
from tests_description.models import TestCase
from tests_representation.models import Test, TestPlan, TestResult

from tests import constants
from tests.commons import RequestType


@pytest.mark.django_db
class TestPlanEndpoints:
    view_name_detail = 'api:v1:testplan-detail'
    view_name_list = 'api:v1:testplan-list'

    def test_list(self, api_client, authorized_superuser, several_test_plans_from_api):
        expected_instances = several_test_plans_from_api
        response = api_client.send_request(self.view_name_list)

        for instance_dict in json.loads(response.content):
            assert instance_dict in expected_instances, f'{instance_dict} was not found in expected instances.'

    def test_retrieve(self, api_client, authorized_superuser, test_plan_from_api):
        response = api_client.send_request(self.view_name_detail, reverse_kwargs={'pk': test_plan_from_api.get('id')})
        actual_dict = json.loads(response.content)
        assert actual_dict == test_plan_from_api, 'Actual model dict is different from expected'

    @pytest.mark.parametrize('number_of_param_groups, number_of_entities_in_group', [(1, 3), (2, 2), (3, 4)])
    def test_creation(self, api_client, authorized_superuser, combined_parameters, project):
        parameters, expected_number_of_plans = combined_parameters
        testplan_dict = {
            'name': 'Test plan',
            'due_date': constants.DATE,
            'started_at': constants.DATE,
            'parameters': parameters,
            'project': project.id
        }
        response = api_client.send_request(self.view_name_list, testplan_dict, HTTPStatus.CREATED, RequestType.POST)
        endpoint_plans = json.loads(response.content)
        actual_parameters_combinations = []
        for plan in endpoint_plans:
            params_from_plan = plan.get('parameters').sort
            assert params_from_plan not in actual_parameters_combinations, 'Found duplicate params in TestPlans'
            actual_parameters_combinations.append(plan.get('parameters'))
        assert TestPlan.objects.count() == expected_number_of_plans, f'Expected number of test plans ' \
                                                                     f'"{expected_number_of_plans}"' \
                                                                     f'actual: "{TestPlan.objects.count()}"'
        assert len(endpoint_plans) == expected_number_of_plans, f'Expected number of test plans from endpoint ' \
                                                                f'"{expected_number_of_plans}"' \
                                                                f'actual: "{len(endpoint_plans)}"'

    @pytest.mark.parametrize('number_of_param_groups, number_of_entities_in_group', [(1, 3), (2, 2), (3, 4)])
    def test_tests_generated_on_create(self, api_client, authorized_superuser, combined_parameters, test_case_factory,
                                       project):
        number_of_cases = 5
        case_ids = [test_case_factory().id for _ in range(number_of_cases)]
        parameters, expected_number_of_plans = combined_parameters
        number_of_tests = number_of_cases * expected_number_of_plans
        testplan_dict = {
            'name': 'Test plan',
            'due_date': constants.DATE,
            'started_at': constants.DATE,
            'parameters': parameters,
            'test_cases': case_ids,
            'project': project.id
        }
        response = api_client.send_request(self.view_name_list, testplan_dict, HTTPStatus.CREATED, RequestType.POST)
        test_plans = json.loads(response.content)
        pk = test_plans[0].get('id')
        assert Test.objects.count() == number_of_tests
        assert TestCase.objects.count() == number_of_cases
        update_dict = {
            'test_cases': case_ids[:-1],
        }
        api_client.send_request(
            self.view_name_detail,
            update_dict,
            HTTPStatus.OK,
            RequestType.PATCH,
            reverse_kwargs={'pk': pk}
        )
        assert Test.objects.count() == number_of_tests - 1, 'More then one test was deleted by updating'
        test_ids = []
        for plan in test_plans:
            test_ids.extend(test.get('id')for test in plan.get('tests'))
        assert len(set(test_ids)) == len(test_ids), 'Test ids from testplans were not unique.'

    @pytest.mark.parametrize(
        'slice_num, expected_number, err_msg',
        [
            (None, 5, 'Number of cases should not change'),
            (1, 1, 'Number of cases was not decreased'),
            (0, 0, 'Cases were found after updating with empty list')
        ],
        ids=['Update with same cases', 'Update to one case', 'Update to 0 cases']
    )
    def test_tests_generated_deleted_on_partial_update(self, api_client, authorized_superuser, test_plan_from_api,
                                                       test_case_factory, slice_num, expected_number, err_msg):
        number_of_cases = 5
        case_ids = [test_case_factory().id for _ in range(number_of_cases)]
        assert not Test.objects.count()
        assert TestCase.objects.count() == number_of_cases
        api_client.send_request(
            self.view_name_detail,
            data={'test_cases': case_ids},
            expected_status=HTTPStatus.OK,
            request_type=RequestType.PATCH,
            reverse_kwargs={'pk': test_plan_from_api.get('id')}
        )
        api_client.send_request(
            self.view_name_detail,
            data={'test_cases': case_ids[:slice_num]},
            expected_status=HTTPStatus.OK,
            request_type=RequestType.PATCH,
            reverse_kwargs={'pk': test_plan_from_api.get('id')}
        )
        assert Test.objects.count() == expected_number, err_msg

    def test_plan_behaviour_on_update(self, api_client, authorized_superuser, test_case_factory, parameter_factory,
                                      test_result_factory, project):
        number_of_cases = 5
        case_ids = [test_case_factory().id for _ in range(number_of_cases)]
        parameters = [parameter_factory(group_name='os').id for _ in range(3)]
        testplan_dict = {
            'name': 'Test plan',
            'due_date': constants.DATE,
            'started_at': constants.DATE,
            'parameters': parameters,
            'test_cases': case_ids,
            'project': project.id
        }
        response = api_client.send_request(self.view_name_list, testplan_dict, HTTPStatus.CREATED, RequestType.POST)
        test_plans = json.loads(response.content)
        test_ids = copy.deepcopy(test_plans[0].get('tests'))
        result_ids = [test_result_factory(test_id=test_ids[0]['id']).id for _ in range(3)]
        expected_number_of_tests = Test.objects.count()
        update_dict = {
            'test_cases': case_ids
        }
        response = api_client.send_request(
            self.view_name_detail,
            update_dict,
            HTTPStatus.OK,
            RequestType.PATCH,
            reverse_kwargs={'pk': test_plans[0].get('id')}
        )
        plan = json.loads(response.content)
        actual_results = []
        for res in TestResult.objects.filter(test=plan.get('tests')[0]['id']):
            actual_results.append(res.id)
        assert actual_results == result_ids, f'Results changed for test with id: {plan.get("tests")[0]["id"]}'
        assert Test.objects.count() == expected_number_of_tests, 'After update number of tests should not change'

    def test_delete(self, api_client, authorized_superuser, test_plan):
        assert TestPlan.objects.count() == 1, 'Test case was not created'
        api_client.send_request(
            self.view_name_detail,
            expected_status=HTTPStatus.NO_CONTENT,
            request_type=RequestType.DELETE,
            reverse_kwargs={'pk': test_plan.pk}
        )
        assert not TestPlan.objects.count(), f'Test plan with id "{test_plan.id}" was not deleted.'
