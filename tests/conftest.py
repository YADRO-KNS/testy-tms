import json

import pytest
from pytest_factoryboy import register

from tests import constants
from http import HTTPStatus
from tests.commons import CustomAPIClient, RequestType
from tests.factories import (
    GroupFactory,
    ParameterFactory,
    ProjectFactory,
    TestCaseFactory,
    TestFactory,
    TestPlanFactory,
    TestResultFactory,
    TestSuiteFactory,
    UserFactory,
)

register(ParameterFactory)
register(ProjectFactory)
register(TestCaseFactory)
register(TestFactory)
register(TestPlanFactory)
register(TestResultFactory)
register(TestSuiteFactory)
register(UserFactory)
register(GroupFactory)


@pytest.fixture
def api_client():
    return CustomAPIClient()


@pytest.fixture
def superuser(user_factory):
    def make_user(**kwargs):
        return user_factory(is_staff=True, is_superuser=True, **kwargs)

    return make_user


@pytest.fixture
def authorized_superuser(api_client, superuser):
    user = superuser()
    api_client.force_login(user)
    return user


@pytest.fixture
def test_plan_by_api(api_client, authorized_superuser, parameter_factory):
    parameters = []
    for _ in range(3):
        parameters.append(parameter_factory(group_name='os').id)

    testplan_dict = {
        "name": f"Test plan",
        "due_date": constants.DATE,
        "started_at": constants.DATE,
        "parameters": parameters
    }
    response = api_client.send_request('api:v1:testplan-list', testplan_dict, HTTPStatus.CREATED, RequestType.POST)
    return json.loads(response.content)[0]


@pytest.fixture
def combined_parameters(number_of_param_groups, number_of_entities_in_group, parameter_factory):
    parameters = []
    for _ in range(number_of_param_groups):
        # params = []
        src_param = parameter_factory()
        parameters.append(src_param.id)
        for _ in range(number_of_entities_in_group - 1):
            parameters.append(parameter_factory(group_name=src_param.group_name).id)
        # param_groups.append(params)
    number_of_combinations = pow(number_of_entities_in_group, number_of_param_groups)
    return parameters, number_of_combinations


@pytest.fixture
def several_test_plans_by_api(api_client, authorized_superuser, parameter_factory, number_of_instances):
    parameters = []
    for _ in range(3):
        parameters.append(parameter_factory().id)

    test_plans = []
    for idx in range(number_of_instances):
        testplan_dict = {
            "name": f"Test plan {idx}",
            "due_date": constants.DATE,
            "started_at": constants.DATE,
            "parameters": parameters
        }
        response = api_client.send_request('api:v1:testplan-list', testplan_dict, HTTPStatus.CREATED, RequestType.POST)
        test_plans.append(json.loads(response.content)[0])

    return test_plans
