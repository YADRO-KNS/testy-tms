from plugins import TestyPluginConfig


class TestrailMigratorConfig(TestyPluginConfig):
    name = 'testrail_migrator'
    verbose_name = 'TestRail migrator'
    description = 'Migrate your data from testrail to testy'
    version = '0.1'
    plugin_base_url = 'migrator'


config = TestrailMigratorConfig
