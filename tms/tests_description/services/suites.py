from dataclasses import dataclass

from core.models import Project
from django.db.models import QuerySet
from tests_description.models import TestSuite


@dataclass
class TestSuiteDto:
    name: str
    project: Project
    parent: TestSuite


class TestSuiteService:

    def suite_create(self, dto: TestSuiteDto) -> TestSuite:
        suite = TestSuite(
            name=dto.name,
            project=dto.project,
            parent=dto.parent
        )
        suite.full_clean()
        suite.save()
        return suite

    def suite_update(self, suite: TestSuite, dto: TestSuiteDto) -> TestSuite:
        suite.name = dto.name
        suite.project = dto.project
        suite.parent = dto.parent
        suite.full_clean()
        suite.save()
        return suite

    def suite_delete(self, suite: TestSuite) -> TestSuite:
        suite.delete()
        return suite

    def suite_retrieve_all(self) -> QuerySet[TestSuite]:
        return TestSuite.objects.all()

    def suite_retrieve_by_id(self, suite_id: int) -> TestSuite:
        return TestSuite.objects.get(pk=suite_id)
