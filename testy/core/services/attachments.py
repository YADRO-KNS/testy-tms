# TestY TMS - Test Management System
# Copyright (C) 2022 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.
import os
from typing import Any, Dict, List, Union

from core.models import Attachment
from core.selectors.attachments import AttachmentSelector


class AttachmentService:
    non_side_effect_fields = [
        'project', 'name', 'filename', 'comment', 'file_extension', 'content_type', 'size', 'object_id', 'user', 'file',
        'url'
    ]

    def attachment_create(self, data: Dict[str, Any], request) -> Union[List[Attachment], str]:
        attachments_instances = []
        for file in request.data.getlist('file'):
            name, extension = os.path.splitext(file.name)
            data.update(
                {
                    'name': name,
                    'filename': file.name,
                    'file_extension': file.content_type,
                    'size': file.size,
                    'user': request.user,
                    'file': file,
                }
            )
            attachments_instances.append(Attachment.model_create(fields=self.non_side_effect_fields, data=data))
        return attachments_instances

    def attachment_set_content_object(self, attachment: Attachment, content_object):
        if attachment.content_object:
            raise ValueError('Attachment already has content object.')
        attachment.content_object = content_object
        attachment.save()
        return attachment

    def attachments_update_content_object(self, attachments, content_object):
        old_attachments = AttachmentSelector().attachment_list_by_parent_object(
            content_object, content_object.id
        )

        for attachment in attachments:
            if attachment not in old_attachments:
                self.attachment_set_content_object(attachment, content_object)

        for old_attachment in old_attachments:
            if old_attachment not in attachments:
                old_attachment.content_type = None
                old_attachment.object_id = None
                old_attachment.save()
