import argparse
import json
import time
from contextlib import contextmanager
from datetime import datetime

from tqdm import tqdm

from testrail_migrator.config import TestrailConfig, TestyConfig, parse_yaml_config
from testrail_migrator.testrail import TestRailClient
from testrail_migrator.testy import TestyClient


@contextmanager
def timer(function_name: str):
    start_time = time.time()
    yield
    print(f'{function_name} took: ', time.time() - start_time)


def parse_args() -> argparse.Namespace:
    """
    Add arguments to cli.

    Returns:
        Arguments
    """
    parser = argparse.ArgumentParser(description='Command-line arguments')
    parser.add_argument('--config-path', action='store', required=True, type=str, help='Path to config file')
    parser.add_argument('--dump-filepath', action='store', required=True, type=str, help='Path to config file')
    arguments = parser.parse_args()
    # logger.options = arguments
    return arguments


def init_tms_clients(config_path: str):
    testrail_cfg = TestrailConfig(**parse_yaml_config(config_path, 'testrail'))
    testrail_client = TestRailClient(testrail_cfg)
    testy_cfg = TestyConfig(**parse_yaml_config(config_path, 'testy'))
    testy_client = TestyClient(testy_cfg)
    return testrail_client, testy_client


def main():
    args = parse_args()
    testrail_client, testy_client = init_tms_clients(args.config_path)

    current_time = datetime.now()
    session_id = current_time.strftime('%s')
    with open(testy_client.config.path_to_session_ids, 'a') as file:
        file.write(json.dumps({current_time.strftime('%B %-d, %Y, %H:%M:%S'): session_id}, indent=2))

    # Testrail part
    # with timer('Exporting project'):
    #     suites_and_cases = testrail_client.get_suites_cases_for_single_project(1)
    # # TODO: добавить превью с настройкой желаемых добавления кейсов и съютов
    # with open(args.dump_filepath, 'w') as file:
    #     file.write(json.dumps(suites_and_cases, indent=2))

    # Testy part
    with timer('Exporting project'):
        project_dict = {
            'name': testy_client.dumpfile['name'],
            'is_archive': testy_client.dumpfile['is_completed'],
            'import_id': session_id
        }
        announcement = testy_client.dumpfile['announcement']
        if announcement:
            project_dict['description'] = announcement
        project = testy_client.create_project(project_dict)

        suites_bar = tqdm(testy_client.dumpfile['suites'])
        suites_bar.set_description('Suites progress')

        for suite_dict in suites_bar:
            suite_data = {
                'name': suite_dict['name'],
                'project': project['id'],
                'import_id': session_id
            }
            suite = testy_client.create_suite(suite_data)

            cases_bar = tqdm(suite_dict['cases'], leave=False)
            cases_bar.set_description(f'Cases from suite "{suite["name"]}" progress')

            for case_dict in cases_bar:
                case_data = {
                    'name': case_dict['title'],
                    'project': project['id'],
                    'suite': suite['id'],
                    'scenario': case_dict['custom_steps'],
                    'import_id': session_id
                }
                setup = case_data.get('custom_preconds')
                if setup:
                    case_data['setup'] = setup
                testy_client.create_case(case_data)


if __name__ == '__main__':
    main()
