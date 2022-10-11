from typing import Any, Dict

from tests_description.models import TestCase


class TestCaseService:
    non_side_effect_fields = ['name', 'project', 'suite', 'setup', 'scenario', 'teardown', 'estimate']

    def case_create(self, data: Dict[str, Any]) -> TestCase:
        return TestCase.model_create(
            fields=self.non_side_effect_fields,
            data=data,
        )

    def case_update(self, case: TestCase, data: Dict[str, Any]) -> TestCase:
        case, _ = case.model_update(
            fields=self.non_side_effect_fields,
            data=data,
        )
        return case
