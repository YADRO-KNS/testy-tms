from django.db.models import QuerySet
from tests_representation.models import TestPlan


class TestPlanSelector:
    def plan_list(self) -> QuerySet[TestPlan]:
        return QuerySet(model=TestPlan).prefetch_related('test_plans').order_by('id')
