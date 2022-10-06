from django.db.models import QuerySet

from tests_representation.models import TestStatus


class TestStatusSelector:
    def status_list(self) -> QuerySet[TestStatus]:
        return TestStatus.objects.all()
