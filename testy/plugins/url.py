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

from django.apps import apps
from django.conf import settings
from django.conf.urls import include
from django.urls import path
from factory.utils import import_object

from . import views

# UI endpoints
plugin_urls = []

# API endpoints
plugin_api_urls = [
    path('', views.PluginsAPIView.as_view(), name='plugins-list')
]

for plugin_path in settings.TESTY_PLUGINS:
    plugin_name = plugin_path.split('.')[-1]
    app = apps.get_app_config(plugin_name)
    base_url = app.plugin_base_url

    # UI endpoints
    try:
        urlpatterns = import_object(module_name=f'{plugin_path}.urls', attribute_name='urlpatterns')
        if urlpatterns:
            plugin_base_url = f'{base_url}/' if base_url else ''
            plugin_urls.append(path(plugin_base_url, include((urlpatterns, app.label))))
    except ModuleNotFoundError as err:
        logging.warning(f'{plugin_name} ui urls were not found.')
        logging.warning(f'SRC error is {err}')

    # API endpoints
    try:
        urlpatterns = import_object(module_name=f'{plugin_path}.api.urls', attribute_name='urlpatterns')
        if urlpatterns:
            plugin_base_url = f'{base_url}/' if base_url else ''
            plugin_api_urls.append(path(f'{plugin_base_url}api/', include((urlpatterns, f"{app.label}-api"))))
    except ModuleNotFoundError as err:
        logging.warning(f'{plugin_name} api urls were not found.')
        logging.warning(f'SRC error is {err}')
