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

from typing import Any, Dict, List

from django.db import transaction
from tests_representation.models import TestPlan
from tests_representation.services.tests import TestService
from tests_representation.utils import combination_parameters


class TestPlanService:
    non_side_effect_fields = ('name', 'parent', 'started_at', 'due_date', 'finished_at', 'is_archive', 'project',)

    def _make_testplan_model(self, data, parameters=None):
        testplan = TestPlan.model_create(
            fields=self.non_side_effect_fields,
            data=data,
            commit=False
        )
        testplan.lft = 0
        testplan.rght = 0
        testplan.tree_id = 0
        testplan.level = 0

        if parameters is not None:
            testplan.parameters = parameters

        return testplan

    @transaction.atomic
    def testplan_create(self, data=Dict[str, Any]) -> List[TestPlan]:
        testplan_objects = []

        if parameters := data.get('parameters', []):
            for combine_parameter in combination_parameters(parameters):
                testplan_objects.append(self._make_testplan_model(data, combine_parameter))
        else:
            testplan_objects.append(self._make_testplan_model(data))

        test_plans = TestPlan.objects.bulk_create(testplan_objects)
        TestPlan.objects.rebuild()

        if test_cases := data.get('test_cases', []):
            TestService().bulk_test_create(test_plans, test_cases)

        return test_plans

    def testplan_bulk_create_with_tests(self, data_list):
        testplan_objects = []
        for data in data_list:
            parameters = [parameter.id for parameter in data.get('parameters')]
            testplan_objects.append(self._make_testplan_model(data, parameters=parameters if parameters else None))
        test_plans = TestPlan.objects.bulk_create(testplan_objects)
        TestPlan.objects.rebuild()
        created_tests = []
        for test_plan, data in zip(test_plans, data_list):
            if data.get('test_cases'):
                created_tests.extend(TestService().bulk_test_create([test_plan], data['test_cases']))
        return created_tests

    def testplan_bulk_create(self, validated_data):
        testplan_objects = []
        for data in validated_data:
            testplan_objects.append(self._make_testplan_model(data))
        test_plans = TestPlan.objects.bulk_create(testplan_objects)
        TestPlan.objects.rebuild()

        return test_plans

    @transaction.atomic
    def testplan_update(self, *, test_plan: TestPlan, data: dict[str, Any]) -> TestPlan:
        test_plan, _ = test_plan.model_update(
            fields=self.non_side_effect_fields,
            data=data,
        )

        if (test_cases := data.get('test_cases')) is not None:  # test_cases may be empty list
            old_test_case_ids = set(TestService().get_testcase_ids_by_testplan(test_plan))
            new_test_case_ids = {tc.id for tc in test_cases}

            # deleting tests
            if delete_test_case_ids := old_test_case_ids - new_test_case_ids:
                TestService().test_delete_by_test_case_ids(test_plan, delete_test_case_ids)

            # creating tests
            if create_test_case_ids := new_test_case_ids - old_test_case_ids:
                cases = [tc for tc in data['test_cases'] if tc.id in create_test_case_ids]
                TestService().bulk_test_create((test_plan,), cases)

        return test_plan

    def testplan_delete(self, *, test_plan) -> None:
        test_plan.delete()
