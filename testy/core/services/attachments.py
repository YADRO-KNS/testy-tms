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
from typing import Any, Dict, List, Union

from django.conf import settings

from core.models import Attachment, Project


class AttachmentService:
    non_side_effect_fields = [
        'project', 'name', 'filename', 'file_extension', 'content_type', 'size', 'object_id', 'user', 'file', 'url'
    ]

    def attachment_create(self, data: Dict[str, Any], request) -> Union[List[Attachment], str]:
        attachments_instances = []
        for file in request.data.getlist('file'):
            file_extension = file.name.split('.')[1]
            if settings.ALLOWED_FILE_EXTENSIONS and file_extension not in settings.ALLOWED_FILE_EXTENSIONS:
                return file.content_type
            parent_object = data['content_type'].get_object_for_this_type(pk=data['object_id'])
            project = parent_object if isinstance(parent_object, Project) else parent_object.project
            data.update(
                {
                    'name': file.name.split('.')[0],
                    'filename': file.name,
                    'file_extension': file.content_type,
                    'size': file.size,
                    'user': request.user,
                    'file': file,
                    'project': project
                }
            )
            attachments_instances.append(Attachment.model_create(fields=self.non_side_effect_fields, data=data))
        return attachments_instances
