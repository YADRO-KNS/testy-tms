from django.db.models import QuerySet
from tests_description.models import TestSuite


class TestSuiteSelector:
    def suite_list(self) -> QuerySet[TestSuite]:
        return TestSuite.objects.all()
