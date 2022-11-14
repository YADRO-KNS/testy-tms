from typing import Any, Dict, List

from core.models import Attachment


class AttachmentService:
    non_side_effect_fields = ['project', 'name', 'filename', 'content_type', 'size', 'plan', 'case', 'result',
                              'user', 'file']

    def attachment_create(self, data: Dict[str, Any], request) -> List[Attachment]:
        attachments_instances = []
        parent_instances = [data.get('case'), data.get('result'), data.get('plan')]
        for file in request.data.getlist('file'):
            data.update(
                {
                    'name': file.name.split('.')[0],
                    'filename': file.name,
                    'content_type': file.content_type,
                    'size': file.size,
                    'user': request.user,
                    'file': file,
                    'project': [elem.project for elem in parent_instances if elem][0]
                }
            )
            attachments_instances.append(Attachment.model_create(fields=self.non_side_effect_fields, data=data))
        return attachments_instances

    def attachment_update(self, attachment: Attachment, data: Dict[str, Any]) -> Attachment:
        attachment, _ = attachment.model_update(
            fields=self.non_side_effect_fields,
            data=data,
        )
        return attachment
