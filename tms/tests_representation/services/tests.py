from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from tests_description.models import TestCase
from tests_representation.models import Test, TestPlan

UserModel = get_user_model()


@dataclass
class TestDto:
    case: TestCase
    plan: TestPlan
    user: UserModel
    is_archive: bool
    created_at: str = None
    updated_at: str = None


class TestService:

    def test_create(self, dto: TestDto) -> Test:
        test = Test(
            case=dto.case,
            plan=dto.plan,
            user=dto.user,
            is_archive=dto.is_archive,
        )
        test.full_clean()
        test.save()
        return test

    def test_update(self, test: Test, dto: TestDto) -> Test:
        test.case = dto.case
        test.plan = dto.plan
        test.user = dto.user
        test.is_archive = dto.is_archive
        test.full_clean()
        test.save()
        return test

    def test_delete(self, test: Test) -> Test:
        test.delete()
        return test

    def test_retrieve_all(self) -> QuerySet[Test]:
        return Test.objects.all()

    def test_retrieve_by_id(self, test_id: int) -> Test:
        return Test.objects.get(pk=test_id)
