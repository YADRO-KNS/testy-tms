from enum import Enum

from django.db.models import QuerySet

from core.models import Attachment


class ParentType(Enum):
    TEST_PLAN = 'plans'
    TEST_CASE = 'cases'
    TEST_RESULT = 'results'


class AttachmentSelector:
    def attachment_list(self) -> QuerySet[Attachment]:
        return Attachment.objects.all()

    def attachment_list_by_parent(self, pk: str, parent_type: ParentType):
        if parent_type == ParentType.TEST_PLAN:
            return Attachment.objects.filter(plan=pk)
        elif parent_type == ParentType.TEST_CASE:
            return Attachment.objects.filter(case=pk)
        elif parent_type == ParentType.TEST_RESULT:
            return Attachment.objects.filter(result=pk)
