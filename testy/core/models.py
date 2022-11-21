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
from django.db import models
from django.utils.translation import gettext_lazy as _

from testy.models import BaseModel

__all__ = (
    'Project',
)


class Project(BaseModel):
    name = models.CharField(_('name'), max_length=settings.CHAR_FIELD_MAX_LEN)
    description = models.TextField(_('description'), blank=True)
    is_archive = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def __str__(self) -> str:
        return self.name


# class ProjectTreeSerializer(ModelSerializer):
#     children = SerializerMethodField()
#     test_cases = SerializerMethodField('get_project_serializer')
#
#     class Meta:
#         model = Project
#         fields = ('name', 'description')
#
#     def get_children(self, value):
#         return self.__class__(value.get_children(), many=True).data
#
#     def get_project_serializer(self, obj):
#         serializer_context = {'request': self.context.get('request')}
#         test_suites = TestSuite.objects.all().filter(suite=obj)
#         serializer = TestSuiteSerializer(test_suites, many=True, context=serializer_context)
#         return serializer.data
