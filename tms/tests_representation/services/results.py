from typing import Any, Dict

from tests_representation.models import TestResult


class TestResultService:
    non_side_effect_fields = ['status', 'test', 'user', 'comment', 'is_archive', 'test_case_version']

    def result_create(self, data: Dict[str, Any]) -> TestResult:
        return TestResult.model_create(
            fields=self.non_side_effect_fields,
            data=data,
            commit=True,
        )

    def result_update(self, result: TestResult, data: Dict[str, Any]) -> TestResult:
        result, has_updated = result.model_update(
            fields=self.non_side_effect_fields,
            data=data,
            commit=True,
        )
        return result
