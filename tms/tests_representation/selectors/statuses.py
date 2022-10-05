from django.db.models import QuerySet
from tests_representation.models import TestStatus


class TestStatusSelector:
    def status_list(self) -> QuerySet[TestStatus]:
        return QuerySet(model=TestStatus).prefetch_related('test_statuses').order_by('id')
