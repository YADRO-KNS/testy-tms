from django.db.models import QuerySet
from tests_description.models import TestCase


class TestCaseSelector:
    def case_list(self) -> QuerySet[TestCase]:
        return TestCase.objects.all()

    def case(self, test_case_id: id) -> TestCase:
        return TestCase.objects.get(pk=test_case_id)

    def case_version(self, case: TestCase) -> int:
        history = case.history.first()
        return history.history_id

    def case_list_for_suite(self, suite_id) -> QuerySet[TestCase]:
        return QuerySet(model=TestCase).filter(suite=suite_id)
