from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    _base_readonly_fields = ("created_at", "updated_at",)

    def get_readonly_fields(self, request, obj=None):
        if self.readonly_fields:
            return self.readonly_fields + self._base_readonly_fields
        else:
            return self._base_readonly_fields
