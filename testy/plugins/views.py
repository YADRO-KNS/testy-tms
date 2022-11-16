from django.apps import apps
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from plugins.utils import parse_plugin_config


class PluginsAPIView(APIView):

    def get(self, request):
        plugin_list = []
        for plugin in settings.TESTY_PLUGINS:
            plugin_list.append(parse_plugin_config(apps.get_app_config(plugin)))
        return Response(plugin_list)
