from django.db.models import QuerySet
from tests_description.models import TestSuite


class TestSuiteSelector:
    def suite_list(self) -> QuerySet[TestSuite]:
        return QuerySet(model=TestSuite).prefetch_related('test_suites').order_by('id')
