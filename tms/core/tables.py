import django_tables2 as tables
from core.models import Project


class ProjectTable(tables.Table):
    remove = tables.TemplateColumn(template_code="""
                                   {% load static %}
                                   <span>
                                        <a href="{% url 'admin_project_delete' record.id %}">
                                            <img src="{% static 'tms/images/trash.svg' %}">
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
                'class': 'table-light'
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
