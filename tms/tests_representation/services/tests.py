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

from typing import Any, Dict

from django.db import transaction
from django.db.models import QuerySet
from tests_description.models import TestCase
from tests_representation.models import Test, TestPlan


class TestService:
    non_side_effect_fields = ['case', 'plan', 'user', 'is_archive', 'project']

    def _make_test_model(self, data):
        return Test.model_create(
            fields=self.non_side_effect_fields,
            data=data,
            commit=False
        )

    def test_create(self, data: Dict[str, Any]) -> Test:
        test = Test.model_create(
            fields=self.non_side_effect_fields,
            data=data,
            commit=False
        )
        test.project = test.case.project
        test.full_clean()
        test.save()
        return test

    @transaction.atomic
    def test_delete_by_test_case_ids(self, test_plan: TestPlan, test_case_ids: list[int]) -> None:
        Test.objects.filter(plan=test_plan).filter(case__in=test_case_ids).delete()

    @transaction.atomic
    def bulk_test_create(self, test_plans: list[TestPlan], cases: list[TestCase]):
        test_objects = [self._make_test_model({'case': case, 'plan': tp, 'project': tp.project}) for tp in test_plans
                        for case in cases]
        return Test.objects.bulk_create(test_objects)

    def test_update(self, test: Test, data: Dict[str, Any]) -> Test:
        test, _ = test.model_update(
            fields=self.non_side_effect_fields,
            data=data,
        )
        return test

    def get_testcase_ids_by_testplan(self, test_plan: TestPlan) -> QuerySet[int]:
        return test_plan.tests.values_list('case', flat=True)
