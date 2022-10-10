import logging
from typing import Any, Dict, List, Tuple

from django.db import models
from django.utils.translation import gettext_lazy as _

from tms.types import DjangoModelType

logger = logging.getLogger(__name__)


class ServiceModelMixin(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def model_create(cls, fields: List[str], data: Dict[str, Any], commit: bool = True) -> DjangoModelType:
        actually_fields = {key: data[key] for key in fields if key in data}
        instance = cls(**actually_fields)

        if commit:
            instance.full_clean()
            instance.save()

        return instance

    def model_update(
            self, fields: List[str], data: Dict[str, Any], commit: bool = True
    ) -> Tuple[DjangoModelType, bool]:
        has_updated = False

        for field in fields:
            if field not in data:
                continue

            if getattr(self, field) != data[field]:
                has_updated = True
                setattr(self, field, data[field])

        if has_updated and commit:
            self.full_clean()
            self.save(update_fields=fields)
        if not has_updated:
            logger.error('Model was not updated.')
        return self, has_updated


class BaseModel(ServiceModelMixin, models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        abstract = True
