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
import django_tables2 as tables
from core.models import Project
from tests_representation.models import Parameter


class ProjectTable(tables.Table):
    remove = tables.TemplateColumn(template_code="""
                                   {% load static %}
                                   <span>
                                        <a href="{% url 'admin_project_delete' record.id %}">
                                            <i class="bi bi-trash" style="color: #000"></i>
                                        </a>
                                   </span>
                                   """,
                                   verbose_name='', orderable=False, extra_context={'href_args': tables.A('pk')},
                                   attrs={'td': {'class': 'text-end'}})

    name = tables.LinkColumn('admin_project_edit', args=[tables.A('pk')])

    class Meta:
        model = Project
        fields = ('name', 'description')
        attrs = {
            'class': 'table table-hover text-small',
            'thead': {
                'class': 'border-bottom',
            },
            'tbody': {
                'class': 'border-light fw-light h6',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ParameterTable(tables.Table):
    remove = tables.TemplateColumn(template_code="""
                                   {% load static %}
                                   <span>
                                        <a href="{% url 'admin_parameter_delete' record.project_id record.id %}">
                                            <i class="bi bi-trash" style="color: #000"></i>
                                        </a>
                                   </span>
                                   """,
                                   verbose_name='',
                                   orderable=False,
                                   extra_context={'href_args': [tables.A('project_id'), tables.A('pk')]},
                                   attrs={'td': {'class': 'text-end'}})
    data = tables.LinkColumn('admin_parameter_edit', args=[tables.A('project_id'), tables.A('pk')])

    class Meta:
        model = Parameter
        fields = ('group_name', 'data')
        attrs = {
            'class': 'table table-hover text-small',
            'thead': {
                'class': 'border-bottom',
            },
            'tbody': {
                'class': 'border-light fw-light h6',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
