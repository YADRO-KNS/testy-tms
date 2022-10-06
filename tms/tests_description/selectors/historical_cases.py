from django.db.models import QuerySet
from tests_description.models import HistoricalTestCase


class HistoricalTestCaseSelector:
    def historical_case_list(self) -> QuerySet[HistoricalTestCase]:
        return HistoricalTestCase.objects.all()
