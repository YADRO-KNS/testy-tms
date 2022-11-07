
from django.db.models import QuerySet
from tests_description.models import TestSuite


class TestSuiteSelector:
    def suite_list(self) -> QuerySet[TestSuite]:
        return TestSuite.objects.all()

    def suite_project_root_list(self, project_id: int) -> QuerySet[TestSuite]:
        return QuerySet(model=TestSuite).filter(project=project_id, parent=None).order_by('name')
