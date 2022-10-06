from django.db.models import QuerySet
from tests_representation.models import TestPlan


class TestPlanSelector:
    def plan_list(self) -> QuerySet[TestPlan]:
        return TestPlan.objects.all()
