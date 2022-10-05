from typing import Any, Dict

from tests_representation.models import TestPlan, TestResult


class TestPlanService:
    non_side_effect_fields = ['parent', 'due_date', 'finished_at', 'is_archive', 'level', 'started_at', 'lft', 'rght',
                              'parameters', 'tree_id']

    def plan_create(self, data: Dict[str, Any]) -> TestPlan:
        return TestPlan.model_create(
            fields=self.non_side_effect_fields,
            data=data,
            commit=True,
        )

    def plan_update(self, plan: TestResult, data: Dict[str, Any]) -> TestPlan:
        plan, has_updated = plan.model_update(
            fields=self.non_side_effect_fields,
            data=data,
            commit=True,
        )
        return plan
