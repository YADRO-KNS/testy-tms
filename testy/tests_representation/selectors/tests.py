
from django.db.models import QuerySet
from tests_representation.models import Test


class TestSelector:
    def test_list(self) -> QuerySet[Test]:
        return Test.objects.all()
