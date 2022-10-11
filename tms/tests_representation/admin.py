from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from tests_representation.models import Test, TestPlan, TestResult

from tms.admin import BaseAdmin


@admin.register(TestPlan)
class TestPlanAdmin(BaseAdmin, MPTTModelAdmin):
    list_display = ('parent', 'started_at', 'due_date', 'finished_at', 'is_archive')
    search_fields = ('id',)


@admin.register(Test)
class TestAdmin(BaseAdmin):
    list_display = ('case', 'plan', 'user', 'is_archive')
    search_fields = ('id',)


@admin.register(TestResult)
class TestResultAdmin(BaseAdmin):
    list_display = ('test', 'status', 'comment', 'user')
    search_fields = ('name',)