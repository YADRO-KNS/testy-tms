from django.db.models import QuerySet
from tests_representation.models import TestResult


class TestResultSelector:
    def result_list(self) -> QuerySet[TestResult]:
        return TestResult.objects.all()
