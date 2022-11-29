import yaml
from dataclasses import dataclass


@dataclass
class TestrailConfig:
    """Config for testrail uploader."""

    login: str = None
    password: str = None
    api_url: str = None


def parse_yaml_config(config_path: str) -> TestrailConfig:
    """
    Parse yaml config file.

    Args:
        config_path: path to config

    Returns:
          Testrail config, Allure config, kwargs for force_passed.
    """
    with open(config_path, 'r') as config_file:
        try:
            config = yaml.safe_load(config_file)
        except yaml.YAMLError as err:
            pass
            # logger.error(str(err))
    return TestrailConfig(**config.get('testrail'))
