from typing import Any, Dict

from tests_representation.models import Test


class TestService:
    non_side_effect_fields = ['case', 'plan', 'user', 'is_archive']

    def test_create(self, data: Dict[str, Any]) -> Test:
        return Test.model_create(
            fields=self.non_side_effect_fields,
            data=data,
        )

    def test_update(self, test: Test, data: Dict[str, Any]) -> Test:
        test, _ = test.model_update(
            fields=self.non_side_effect_fields,
            data=data,
        )
        return test