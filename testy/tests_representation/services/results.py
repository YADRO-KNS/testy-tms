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

from typing import Any, Dict

from django.db import transaction
from tests_description.selectors.cases import TestCaseSelector
from tests_representation.models import TestResult
from users.models import User


class TestResultService:
    non_side_effect_fields = ['status', 'user', 'test', 'comment', 'is_archive', 'test_case_version', 'execution_time']

    @transaction.atomic
    def result_create(self, data: Dict[str, Any], user: User) -> TestResult:
        test_result: TestResult = TestResult.model_create(
            fields=self.non_side_effect_fields,
            data=data,
            commit=False,
        )
        test_result.user = user
        test_result.project = test_result.test.case.project
        test_result.test_case_version = TestCaseSelector().case_version(test_result.test.case)
        test_result.full_clean()
        test_result.save()

        return test_result

    def create_bulk_results(self, data_list):
        # TODO: убрать двухэтажные компрехеншены
        fields = self.non_side_effect_fields
        fields.append('project')
        test_objects = [TestResult.model_create(fields=fields, data=data, commit=False) for data in
                        data_list]
        return TestResult.objects.bulk_create(test_objects)

    @transaction.atomic
    def result_update(self, test_result: TestResult, data: Dict[str, Any]) -> TestResult:
        test_result, has_updated = test_result.model_update(
            fields=self.non_side_effect_fields,
            data=data,
            commit=False,
        )

        if has_updated:
            test_result.test_case_version = TestCaseSelector().case_version(test_result.test.case)
        test_result.full_clean()
        test_result.save()

        return test_result
