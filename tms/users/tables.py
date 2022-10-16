import django_tables2 as tables
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserTable(tables.Table):
    remove_user = tables.TemplateColumn(template_code="""
                                        {% load static %}
                                        <span>
                                            <a href="{% url 'admin_user_delete' record.id %}">
                                                <img src="{% static 'tms/images/trash.svg' %}">
                                            </a>
                                        </span>
                                        """,
                                        verbose_name='', orderable=False, extra_context={'href_args': tables.A('pk')},
                                        attrs={'td': {'class': 'text-end'}})

    username = tables.LinkColumn('admin_user_profile', args=[tables.A('pk')])

    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser')
        attrs = {
            'class': 'table table-hover text-small',
            'thead': {
                'class': 'table-light'
            },
            'td': {
                'remove_user': {
                    'class': 'text-end'
                }
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
