
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from tests_description.models import TestCase, TestSuite

from testy.admin import BaseAdmin


@admin.register(TestSuite)
class TestSuiteAdmin(BaseAdmin, MPTTModelAdmin):
    list_display = ('name', 'project', 'parent',)
    search_fields = ('name',)


@admin.register(TestCase)
class TestCaseAdmin(BaseAdmin):
    list_display = ('name', 'project', 'suite', )
    search_fields = ('name',)
