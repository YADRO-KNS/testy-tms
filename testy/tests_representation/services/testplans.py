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
    non_side_effect_fields = (
        'name', 'parent', 'started_at', 'due_date', 'finished_at', 'is_archive', 'project', 'description'
    )

    @transaction.atomic
    def testplan_create(self, data=Dict[str, Any]) -> List[TestPlan]:
        test_plan = TestPlan.model_create(fields=self.non_side_effect_fields, data=data)
        if test_cases := data.get('test_cases', []):
            TestService().bulk_test_create([test_plan], test_cases)
        parent = data.get('parent') if data.get('parent') else test_plan
        TestPlan.objects.partial_rebuild(parent.tree_id)
        return test_plan

    @transaction.atomic
    def testplan_bulk_create(self, data=Dict[str, Any]) -> List[TestPlan]:
        parameters = data.get('parameters')
        test_plans = []
        for combine_parameter in combination_parameters(parameters):
            test_plan_object = TestPlan.model_create(fields=self.non_side_effect_fields, data=data, commit=False)
            test_plan_object.parameters = combine_parameter
            test_plan_object.save()
            test_plans.append(test_plan_object)

        if test_cases := data.get('test_cases', []):
            TestService().bulk_test_create(test_plans, test_cases)

        if parent := data.get('parent'):
            TestPlan.objects.partial_rebuild(parent.tree_id)
        else:
            for test_plan in test_plans:
                TestPlan.objects.partial_rebuild(test_plan.tree_id)
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
        TestPlan.objects.partial_rebuild(test_plan.tree_id)
        return test_plan

    def testplan_delete(self, *, test_plan) -> None:
        test_plan.delete()
