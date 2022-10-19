from typing import Optional

from django.db.models import QuerySet

from tests_representation.models import TestPlan
import logging

logger = logging.getLogger(__name__)


class TestPlanSelector:
    def testplan_list(self) -> QuerySet[TestPlan]:
        return TestPlan.objects.all()

    def testplan_get_by_pk(self, pk) -> Optional[TestPlan]:
        return TestPlan.objects.get(pk=pk)
