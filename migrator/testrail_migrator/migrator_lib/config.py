from dataclasses import dataclass

import yaml


@dataclass
class TestrailConfig:
    """Config for testrail uploader."""

    login: str = None
    password: str = None
    api_url: str = None
    dumpfile_path: str = None


@dataclass
class TestyConfig:
    login: str = None
    password: str = None
    api_url: str = None
    dumpfile_path: str = None
    path_to_session_ids: str = None


def parse_yaml_config(config_path: str, config_name: str):
    """
    Parse yaml config file.

    Args:
        config_path: path to config
        config_name: key in yaml dict

    Returns:
          Testrail config, Allure config, kwargs for force_passed.
    """
    with open(config_path, 'r') as config_file:
        try:
            config = yaml.safe_load(config_file)
        except yaml.YAMLError as err:
            pass
            # logger.error(str(err))
    return config.get(config_name)
