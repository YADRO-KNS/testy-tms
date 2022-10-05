from typing import Any, Dict

from tests_description.models import HistoricalTestCase


class HistoricalTestCaseService:
    non_side_effect_fields = ['history_user', 'project', 'suite', 'estimate', 'history_change_reason', 'history_date',
                              'history_type', 'id', 'name', 'scenario', 'setup', 'teardown']

    def historical_case_create(self, data: Dict[str, Any]) -> HistoricalTestCase:
        return HistoricalTestCase.model_create(
            fields=self.non_side_effect_fields,
            data=data,
            commit=True,
        )

    def historical_case_suite_update(
            self,
            historical_case: HistoricalTestCase,
            data: Dict[str, Any]
    ) -> HistoricalTestCase:
        historical_case, has_updated = historical_case.model_update(
            fields=self.non_side_effect_fields,
            data=data,
            commit=True,
        )
        return historical_case
