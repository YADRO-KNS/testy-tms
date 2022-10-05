from django.db.models import QuerySet
from tests_representation.models import TestResult


class TestResultSelector:
    def result_list(self) -> QuerySet[TestResult]:
        return QuerySet(model=TestResult).prefetch_related('test_results').order_by('id')
