import importlib

from django.core.exceptions import ImproperlyConfigured
from packaging import version


def insert_plugins(testy_plugins, installed_plugins, middleware, testy_version):
    for plugin_name in testy_plugins:
        try:
            plugin = importlib.import_module(plugin_name)
        except ModuleNotFoundError as err:
            if err.name == plugin_name:
                raise ImproperlyConfigured(
                    f'Unable to import plugin {plugin_name}: did you forget to install wanted plugin?'
                )
            raise err

        current_version = version.parse(testy_version)

        try:
            plugin_config = plugin.config
        except AttributeError:
            raise ImproperlyConfigured(
                f'You forgot to instantiate config for plugin {plugin_name} after overriding default config'
            )

        installed_plugins.append(f'{plugin_config.__module__}.{plugin_config.__name__}')

        if plugin_config.min_version:
            if current_version < version.parse(plugin_config.min_version):
                raise ImproperlyConfigured(
                    f'Plugin {plugin_config.__module__} requires NetBox minimum version {plugin_config.min_version}.'
                )

        if plugin_config.max_version:
            if current_version > version.parse(plugin_config.max_version):
                raise ImproperlyConfigured(
                    f'Plugin {plugin_config.__module__} requires NetBox maximum version {plugin_config.max_version}.'
                )

        plugin_middleware = plugin_config.middleware
        middleware.extend(plugin_middleware)

    return installed_plugins, middleware
