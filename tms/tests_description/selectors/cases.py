from django.db.models import QuerySet

from tests_description.models import TestCase


class TestCaseSelector:
    def case_list(self) -> QuerySet[TestCase]:
        return TestCase.objects.all()
