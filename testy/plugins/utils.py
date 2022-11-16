def parse_plugin_config(plugin_config):
    return {
        'name': plugin_config.verbose_name,
        'package': plugin_config.name,
        'author': plugin_config.author,
        'author_email': plugin_config.author_email,
        'description': plugin_config.description,
        'version': plugin_config.version
    }
