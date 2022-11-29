import argparse

from testrail_migration.config import parse_yaml_config
from testrail_migration.testrail import TestRailClient


def parse_args() -> argparse.Namespace:
    """
    Add arguments to cli.

    Returns:
        Arguments
    """
    parser = argparse.ArgumentParser(description='Command-line arguments')
    parser.add_argument('--config-path', action='store', required=True, type=str, help='Path to config file')
    arguments = parser.parse_args()
    # logger.options = arguments
    return arguments


def main():
    args = parse_args()
    # logger.info(f'Config is set to {args.config_path}')
    # logger.info(f'Allure report is set to {args.allure_url}')
    testrail_cfg = parse_yaml_config(args.config_path)
    client = TestRailClient(testrail_cfg)

    projects = client.get_all_suites_for_project()
    print()


if __name__ == '__main__':
    main()


