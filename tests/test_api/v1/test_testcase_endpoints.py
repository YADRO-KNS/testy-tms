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
from django.forms import model_to_dict
from tests_description.api.v1.serializers import TestCaseSerializer
from tests_description.models import TestCase

from tests import constants
from tests.commons import RequestType, model_to_dict_via_serializer
from tests.error_messages import REQUIRED_FIELD_MSG
from tests.factories import ProjectFactory, TestSuiteFactory


@pytest.mark.django_db
class TestCaseEndpoints:
    view_name_detail = 'api:v1:testcase-detail'
    view_name_list = 'api:v1:testcase-list'

    def test_list(self, api_client, authorized_superuser, test_case_factory):
        expected_instances = []
        for _ in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
            expected_dict = model_to_dict(test_case_factory())
            expected_dict['attachments'] = []
            expected_dict['key'] = expected_dict['id']
            expected_dict['value'] = expected_dict['id']
            expected_instances.append(expected_dict)

        response = api_client.send_request(self.view_name_list)

        for instance_dict in json.loads(response.content):
            instance_dict.pop('url')
            assert instance_dict in expected_instances, f'{instance_dict} was not found in expected instances.'

    def test_retrieve(self, api_client, authorized_superuser, test_case):
        expected_dict = model_to_dict(test_case)
        expected_dict['attachments'] = []
        response = api_client.send_request(self.view_name_detail, reverse_kwargs={'pk': test_case.pk})
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
        api_client.send_request(self.view_name_list, case_dict, HTTPStatus.CREATED, RequestType.POST)
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

    def test_delete(self, api_client, authorized_superuser, test_case):
        assert TestCase.objects.count() == 1, 'Test case was not created'
        api_client.send_request(
            self.view_name_detail,
            expected_status=HTTPStatus.NO_CONTENT,
            request_type=RequestType.DELETE,
            reverse_kwargs={'pk': test_case.pk}
        )
        assert not TestCase.objects.count(), f'TestCase with id "{test_case.id}" was not deleted.'


@pytest.mark.django_db
class TestCaseEndpointsQueryParams:
    view_name_list = 'api:v1:testcase-list'

    @pytest.mark.parametrize(
        'field_name, factory',
        [('project', ProjectFactory), ('suite', TestSuiteFactory)],
        ids=['TestCase filter by project query param', 'TestCase filter by suite query param']
    )
    def test_case_filter(self, api_client, authorized_superuser, test_case_factory, field_name, factory):
        instances = [factory() for _ in range(3)]
        for _ in range(2):
            for instance in instances:
                test_case_factory(**{field_name: instance})
        for instance in instances:
            filtered_instances = TestCase.objects.filter(**{field_name: instance.id})
            expected_dict = model_to_dict_via_serializer(
                filtered_instances,
                serializer_class=TestCaseSerializer,
                many=True
            )
            response = api_client.send_request(
                self.view_name_list,
                expected_status=HTTPStatus.OK,
                request_type=RequestType.GET,
                query_params={field_name: instance.id}
            )
            actual_dict = json.loads(response.content)
            assert actual_dict == expected_dict, 'Actual and expected dict are different.'
