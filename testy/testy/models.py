# TestY TMS - Test Management System
# Copyright (C) 2022 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.

import logging
from typing import Any, Dict, List, Tuple

from django.db import models
from django.utils.translation import gettext_lazy as _

from testy.types import DjangoModelType

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
