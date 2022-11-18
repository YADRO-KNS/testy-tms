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
