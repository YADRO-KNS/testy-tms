from django.db.models import QuerySet
from tests_representation.models import Test


class TestSelector:
    def test_list(self) -> QuerySet[Test]:
        return QuerySet(model=Test).prefetch_related('tests').order_by('id')
