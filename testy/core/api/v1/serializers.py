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
from core.models import Attachment, Project
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import HyperlinkedIdentityField, ModelSerializer

__all__ = (
    'ProjectSerializer'
)


class ProjectSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:project-detail')

    class Meta:
        model = Project
        fields = ('id', 'url', 'name', 'description', 'is_archive')


class AttachmentSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:attachment-detail')

    class Meta:
        model = Attachment
        fields = (
            'project', 'comment',
            'name', 'filename', 'file_extension', 'size', 'content_type', 'object_id', 'user', 'file', 'url'
        )

        read_only_fields = ('name', 'filename', 'file_extension', 'size', 'user', 'url')

    def validate(self, attrs):
        content_type = attrs.get('content_type')
        object_id = attrs.get('object_id')

        if content_type is None:
            return attrs

        if not content_type.model_class().objects.all().filter(pk=object_id):
            raise ValidationError(f'Specified model does not have object with id {object_id}')

        return attrs
