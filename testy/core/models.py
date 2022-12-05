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


from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy

from testy.models import BaseModel

__all__ = (
    'Project',
    'Attachment'
)

from validators import ExtensionValidator, ProjectValidator

from utils import get_attachments_file_path

UserModel = get_user_model()


class Project(BaseModel):
    name = models.CharField('name', max_length=settings.CHAR_FIELD_MAX_LEN)
    description = models.TextField('description', blank=True)
    is_archive = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        verbose_name = gettext_lazy('project')
        verbose_name_plural = gettext_lazy('projects')

    def __str__(self) -> str:
        return self.name


class Attachment(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # Name of file without extension
    name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    # Full filename
    filename = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    file_extension = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    # Size of file in bytes
    size = models.PositiveBigIntegerField()
    # Parent object table, example: core_project
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        validators=[ProjectValidator()]
    )
    # Id of object from table of content_type
    object_id = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    # Instance of parent object
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    file = models.FileField(
        max_length=150,
        upload_to=get_attachments_file_path,
        validators=[ExtensionValidator()]
    )

    def __str__(self):
        return str(self.file.url)
