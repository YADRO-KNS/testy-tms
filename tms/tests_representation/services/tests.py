from typing import Any, Dict
from django.db import transaction
from django.db.models import QuerySet

from tests_description.models import TestCase
from tests_representation.models import Test, TestPlan


class TestService:
    non_side_effect_fields = ['case', 'plan', 'user', 'is_archive']

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
        test_objects = [self._make_test_model({'case': case, 'plan': tp}) for tp in test_plans for case in cases]
        return Test.objects.bulk_create(test_objects)

    def test_update(self, test: Test, data: Dict[str, Any]) -> Test:
        test, _ = test.model_update(
            fields=self.non_side_effect_fields,
            data=data,
        )
        return test

    def get_testcase_ids_by_testplan(self, test_plan: TestPlan) -> QuerySet[int]:
        return test_plan.tests.values_list('case', flat=True)
