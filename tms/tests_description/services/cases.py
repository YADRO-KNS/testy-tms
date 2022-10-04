from dataclasses import dataclass

from core.models import Project
from django.db.models import QuerySet
from tests_description.models import TestCase, TestSuite


@dataclass
class TestCaseDto:
    name: str
    project: Project
    suite: TestSuite
    setup: str
    scenario: str
    teardown: str
    estimate: int


class TestCaseService:

    def case_create(self, dto: TestCaseDto) -> TestCase:
        case = TestCase(
            name=dto.name,
            project=dto.project,
            suite=dto.suite,
            setup=dto.setup,
            scenario=dto.scenario,
            teardown=dto.teardown,
            estimate=dto.estimate
        )
        case.full_clean()
        case.save()
        return case

    def case_update(self, case: TestCase, dto: TestCaseDto) -> TestCase:
        case.name = dto.name
        case.project = dto.project
        case.suite = dto.suite
        case.setup = dto.setup
        case.scenario = dto.scenario
        case.teardown = dto.teardown
        case.estimate = dto.estimate
        case.full_clean()
        case.save()
        return case

    def case_delete(self, case: TestCase) -> TestCase:
        case.delete()
        return case

    def case_retrieve_all(self) -> QuerySet[TestCase]:
        return TestCase.objects.all()

    def case_retrieve_by_id(self, case_id: int) -> TestCase:
        return TestCase.objects.get(pk=case_id)
