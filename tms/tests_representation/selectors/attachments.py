from django.db.models import QuerySet
from tests_representation.models import Attachment


class AttachmentSelector:
    def attachment_list(self) -> QuerySet[Attachment]:
        return Attachment.objects.all()
