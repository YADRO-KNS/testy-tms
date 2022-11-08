# TestY TMS - Test Management System
# Copyright (C) 2022 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.

import json
from http import HTTPStatus

import pytest
from pytest_factoryboy import register

from tests import constants
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
def test_plan_from_api(api_client, authorized_superuser, test_plan):
    response = api_client.send_request('api:v1:testplan-detail', reverse_kwargs={'pk': test_plan.id})
    return json.loads(response.content)


@pytest.fixture
def combined_parameters(number_of_param_groups, number_of_entities_in_group, parameter_factory):
    parameters = []
    for _ in range(number_of_param_groups):
        src_param = parameter_factory()
        parameters.append(src_param.id)
        for _ in range(number_of_entities_in_group - 1):
            parameters.append(parameter_factory(group_name=src_param.group_name).id)
    number_of_combinations = pow(number_of_entities_in_group, number_of_param_groups)
    return parameters, number_of_combinations


@pytest.fixture
def several_test_plans_from_api(api_client, authorized_superuser, parameter_factory, project):
    parameters = []
    for _ in range(3):
        parameters.append(parameter_factory().id)

    test_plans = []
    for idx in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
        testplan_dict = {
            'name': f'Test plan {idx}',
            'due_date': constants.DATE,
            'started_at': constants.DATE,
            'parameters': parameters,
            'project': project.id
        }
        response = api_client.send_request('api:v1:testplan-list', testplan_dict, HTTPStatus.CREATED, RequestType.POST)
        test_plans.append(json.loads(response.content)[0])

    return test_plans
