from typing import Any, Dict

from tests_description.models import TestSuite


class TestSuiteService:
    non_side_effect_fields = ['parent', 'project', 'name', 'level', 'lft', 'rght', 'tree_id']

    def suite_create(self, data: Dict[str, Any]) -> TestSuite:
        return TestSuite.model_create(
            fields=self.non_side_effect_fields,
            data=data,
            commit=True,
        )

    def suite_update(self, suite: TestSuite, data: Dict[str, Any]) -> TestSuite:
        suite, has_updated = suite.model_update(
            fields=self.non_side_effect_fields,
            data=data,
            commit=True,
        )
        return suite
