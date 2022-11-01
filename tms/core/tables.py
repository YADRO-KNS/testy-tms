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
                                        <a href="{% url 'admin_parameter_delete' record.id %}">
                                            <i class="bi bi-trash" style="color: #000"></i>
                                        </a>
                                   </span>
                                   """,
                                   verbose_name='', orderable=False, extra_context={'href_args': tables.A('pk')},
                                   attrs={'td': {'class': 'text-end'}})

    group_name = tables.LinkColumn('admin_parameter_edit', args=[tables.A('pk')])

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
