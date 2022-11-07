import django_tables2 as tables
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserTable(tables.Table):
    remove_user = tables.TemplateColumn(template_code="""
                                        {% load static %}
                                        <span>
                                            <a href="{% url 'admin_user_delete' record.id %}">
                                                <i class="bi bi-trash" style="color: #000"></i>
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
                'class': 'border-bottom',
            },
            'tbody': {
                'class': 'border-light fw-light h6',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
