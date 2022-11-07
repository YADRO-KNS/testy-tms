
from core.models import Project
from django.contrib import admin

from testy.admin import BaseAdmin


@admin.register(Project)
class ProjectAdmin(BaseAdmin):
    list_display = ('name',)
    search_fields = ('name',)
