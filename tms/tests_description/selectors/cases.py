from django.db.models import QuerySet
from tests_description.models import TestCase


class TestCaseSelector:
    def case_list(self) -> QuerySet[TestCase]:
        return TestCase.objects.all()

    def case_version(self, case: TestCase) -> int:
        history = case.history.first()
        return history.history_id
