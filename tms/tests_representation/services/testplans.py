from typing import Any, Dict, List

from django.db import transaction
from tests_representation.models import TestPlan
from tests_representation.services.tests import TestService
from tests_representation.utils import combination_parameters


class TestPLanService:
    non_side_effect_fields = ('name', 'parent', 'started_at', 'due_date', 'finished_at', 'is_archive',)

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
            combine_parameters = combination_parameters(parameters)

            for combine_parameter in combine_parameters:
                testplan_objects.append(self._make_testplan_model(data, combine_parameter))
        else:
            testplan_objects.append(self._make_testplan_model(data))

        test_plans = TestPlan.objects.bulk_create(testplan_objects)
        TestPlan.objects.rebuild()

        if test_cases := data.get('test_cases', []):
            TestService().bulk_test_create(test_plans, test_cases)

        return test_plans

    @transaction.atomic
    def testplan_update(self, *, test_plan: TestPlan, data: dict[str, Any]) -> TestPlan:
        test_plan, _ = test_plan.model_update(
            fields=self.non_side_effect_fields,
            data=data,
        )

        if (test_cases := data.get('test_cases', None)) is not None:
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
