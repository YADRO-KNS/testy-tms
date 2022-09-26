from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from tms.models import BaseModel

__all__ = (
    'Project',
)


class Project(BaseModel):
    name = models.CharField(_('name'), max_length=settings.CHAR_FIELD_MAX_LEN)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def __str__(self) -> str:
        return self.name
