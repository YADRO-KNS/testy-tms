from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from users.models import Group as Group_
from users.models import User

admin.site.unregister(Group)


@admin.register(Group_)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_count')
    ordering = ('name',)
    search_fields = ('name',)

    @staticmethod
    def user_count(obj):
        return obj.user_set.count()


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active'
    ]
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email')}),
        ('Groups', {'fields': ('groups',)}),
        ('Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('groups',)
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups__name')
