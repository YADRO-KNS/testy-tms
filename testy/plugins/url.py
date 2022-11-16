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
    except ModuleNotFoundError:
        logging.warning(f'{plugin_name} ui urls were not found.')

    # API endpoints
    try:
        urlpatterns = import_object(module_name=f'{plugin_path}.api.urls', attribute_name='urlpatterns')
        if urlpatterns:
            plugin_base_url = f'{base_url}/' if base_url else ''
            plugin_api_urls.append(path(f'{plugin_base_url}api/', include((urlpatterns, f"{app.label}-api"))))
    except ModuleNotFoundError:
        logging.warning(f'{plugin_name} api urls were not found.')
