from dataclasses import dataclass

from tests_representation.models import TestPlan


# from django.contrib.auth import get_user_model
#
# UserModel = get_user_model()


@dataclass
class TestPlanDto:
    parent: TestPlan
    started_at: str
    due_date: str
    finished_at: str
    is_archive: bool
    created_at: str = None
    updated_at: str = None


class TestPlanService:

    def plan_create(self, dto: TestPlanDto) -> TestPlan:
        plan = TestPlan(
            parent=dto.parent,
            started_at=dto.started_at,
            due_date=dto.due_date,
            finished_at=dto.finished_at,
            is_archive=dto.is_archive
        )
        plan.full_clean()
        plan.save()
        return plan

    def plan_update(self, plan: TestPlan, dto: TestPlanDto):
        plan.parent = dto.parent
        plan.started_at = dto.started_at
        plan.due_date = dto.due_date
        plan.finished_at = dto.finished_at
        plan.is_archive = dto.is_archive
        plan.full_clean()
        plan.save()
        return plan

    def plan_delete(self, plan: TestPlan):
        plan.delete()
        return plan

    def plan_retrieve_all(self):
        return TestPlan.objects.all()

    def plan_retrieve_by_id(self, plan_id: int):
        return TestPlan.objects.get(pk=plan_id)
