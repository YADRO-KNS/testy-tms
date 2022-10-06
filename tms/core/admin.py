from django.contrib import admin

from core.models import Project
from tms.admin import BaseAdmin


@admin.register(Project)
class ProjectAdmin(BaseAdmin):
    list_display = ('name',)
    search_fields = ('name',)
