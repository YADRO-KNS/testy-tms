from django.apps import AppConfig


class TestyPluginConfig(AppConfig):
    name = ''
    verbose_name = ''
    description = ''
    version = ''
    plugin_base_url = ''  # Можно указать базовый урл чтобы все юрлы апи были сгрупированы под ним
    author = ''
    author_email = ''
    middleware = []
    min_version = None
    max_version = None
