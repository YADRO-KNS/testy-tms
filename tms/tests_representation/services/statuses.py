from typing import Any, Dict

from tests_representation.models import TestStatus


class TestStatusService:
    non_side_effect_fields = ['name', 'status_code']

    def status_create(self, data: Dict[str, Any]) -> TestStatus:
        return TestStatus.model_create(
            fields=self.non_side_effect_fields,
            data=data,
            commit=True,
        )

    def status_update(self, status: TestStatus, data: Dict[str, Any]) -> TestStatus:
        status, has_updated = status.model_update(
            fields=self.non_side_effect_fields,
            data=data,
            commit=True,
        )
        return status
