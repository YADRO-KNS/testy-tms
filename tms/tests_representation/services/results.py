from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from tests_representation.models import Test, TestResult

UserModel = get_user_model()


@dataclass
class TestResultDto:
    test: Test
    status: int
    comment: str
    user: UserModel
    is_archive: bool
    created_at: str = None
    updated_at: str = None


class TestResultService:
    def result_create(self, dto: TestResultDto) -> TestResult:
        result = TestResult(
            test=dto.test,
            status=dto.status,
            comment=dto.comment,
            user=dto.user,
            is_archive=dto.is_archive,
        )
        result.full_clean()
        result.save()
        return result

    def result_update(self, result: TestResult, dto: TestResultDto) -> TestResult:
        result.test = dto.test,
        result.status = dto.status,
        result.comment = dto.comment,
        result.user = dto.user,
        result.is_archive = dto.is_archive,
        result.full_clean()
        result.save()
        return result

    def result_delete(self, result: TestResult) -> TestResult:
        result.delete()
        return result

    def result_retrieve_all(self) -> QuerySet[TestResult]:
        return TestResult.objects.all()

    def result_retrieve_by_id(self, result_id: int) -> TestResult:
        return TestResult.objects.get(pk=result_id)
