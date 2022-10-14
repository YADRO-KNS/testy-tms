from django.db.models import QuerySet
from tests_representation.models import TestResult


class TestResultSelector:
    def result_list(self) -> QuerySet[TestResult]:
        return TestResult.objects.all()

    def result_list_by_test_id(self, test_id) -> QuerySet[TestResult]:
        return TestResult.objects.select_related('test').filter(test_id=test_id)
