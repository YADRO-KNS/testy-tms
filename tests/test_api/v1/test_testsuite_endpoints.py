# TMS - Test Management System
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
from tests_description.models import TestSuite

from tests import constants
from tests.commons import RequestType
from tests.error_messages import REQUIRED_FIELD_MSG


@pytest.mark.django_db
class TestSuiteEndpoints:
    view_name_list = 'api:v1:testsuite-list'
    view_name_detail = 'api:v1:testsuite-detail'

    def test_list(self, api_client, authorized_superuser, test_suite_factory):
        expected_instances = []
        for _ in range(constants.NUMBER_OF_OBJECTS_TO_CREATE):
            expected_dict = model_to_dict(test_suite_factory())
            expected_dict['test_cases'] = []
            expected_instances.append(expected_dict)

        response = api_client.send_request(self.view_name_list)
        for instance_dict in json.loads(response.content):
            instance_dict.pop('url')
            assert instance_dict in expected_instances, f'{instance_dict} was not found in expected instances.'

    def test_retrieve(self, api_client, authorized_superuser, test_suite):
        expected_dict = model_to_dict(test_suite)
        expected_dict['test_cases'] = []
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
