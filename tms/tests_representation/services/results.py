from typing import Any, Dict

from django.db import transaction
from tests_description.selectors.cases import TestCaseSelector
from tests_representation.models import Test, TestResult


class TestResultService:
    non_side_effect_fields = ['status', 'user', 'comment', 'is_archive', 'test_case_version']

    @transaction.atomic
    def result_create(self, data: Dict[str, Any], test_id: int) -> TestResult:
        test_result: TestResult = TestResult.model_create(
            fields=self.non_side_effect_fields,
            data=data,
            commit=False,
        )
        test_result.test = Test.objects.get(pk=test_id)
        test_result.project = test_result.test.case.project
        test_result.test_case_version = TestCaseSelector().case_version(test_result.test.case)
        test_result.full_clean()
        test_result.save()

        return test_result

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
