import argparse
import asyncio
import itertools
import json
import logging
import time
from contextlib import contextmanager
from datetime import datetime
from typing import Any

from asgiref.sync import sync_to_async
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model

from tests_representation.services.parameters import ParameterService
from .migrator_lib import TestRailClient, TestrailConfig, TestyClient, TestyConfig, parse_yaml_config
from tqdm import tqdm

from core.models import Project
from tests_description.api.v1.serializers import TestSuiteSerializer, TestCaseSerializer
from tests_description.models import TestSuite
from tests_description.services.cases import TestCaseService
from tests_description.services.suites import TestSuiteService
from tests_representation.api.v1.serializers import TestPlanInputSerializer, TestSerializer, TestResultSerializer
from tests_representation.services.results import TestResultService
from tests_representation.services.testplans import TestPLanService
from tests_representation.services.tests import TestService
from .serializers import ParameterSerializer


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


def get_suites_cases_from_tr(testrail_client: TestRailClient, dump_filepath, from_dump: bool = False):
    # TODO: use filepath and not constant
    if from_dump:
        with open(
                f'/Users/r.kabaev/Desktop/testrail_migrator/backup_suites_cases/resulting2022-12-05 13:59:13.870764.json',
                'r') as file:
            return json.loads(file.read())

    suites_and_cases = testrail_client.get_suites_cases_for_project(1)
    with open(f'/Users/r.kabaev/Desktop/testrail_migrator/backup_suites_cases/resulting{datetime.now()}.json',
              'w') as file:
        file.write(json.dumps(suites_and_cases, indent=2))
    return suites_and_cases


async def upload_suites_cases_to_testy(testy_client: TestyClient):
    current_time = datetime.now()
    session_id = current_time.strftime('%s')
    case_mappings = []

    with open(testy_client.config.path_to_session_ids, 'a') as file:
        file.write(json.dumps({current_time.strftime('%B %-d, %Y, %H:%M:%S'): session_id}, indent=2))

    with timer('Exporting project'):
        project_dict = {
            'name': testy_client.dumpfile['name'],
            'is_archive': testy_client.dumpfile['is_completed'],
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
            }
            suite = testy_client.create_suite(suite_data)

            cases_bar = tqdm(suite_dict['cases'], leave=False)
            cases_bar.set_description(f'Cases from suite "{suite["name"]}" progress')
            tasks = []
            for case_dict in cases_bar:
                case_data = {
                    'name': case_dict['title'],
                    'project': project['id'],
                    'suite': suite['id'],
                    'scenario': case_dict['custom_steps'],
                }
                setup = case_data.get('custom_preconds')
                if setup:
                    case_data['setup'] = setup
                # case_mappings.append(testy_client.create_case(case_data, case_dict['id']))
                tasks.append(
                    asyncio.create_task(
                        testy_client.create_case_async(case_data, case_dict['id'])
                    )
                )

            case_mappings.extend(await asyncio.gather(*tasks))
    return case_mappings


def split_list_by_chunks(src_list: list, chunk_size: int = 40):
    return [src_list[x:x + chunk_size] for x in range(0, len(src_list), chunk_size)]


def find_idx_by_key_value(key: str, value: Any, src_list: list):
    for idx, elem in enumerate(src_list):
        if elem[key] == value:
            return idx


async def get_tests_results_by_run(testrail_client, runs):
    runs_chunks = split_list_by_chunks(runs, 100)
    tests = []
    for idx, chunk in enumerate(runs_chunks):
        print(f'Started processing chunk {idx} of {len(runs_chunks)} of runs')
        tasks = []
        for run in chunk:
            tasks.append(asyncio.create_task(testrail_client.get_tests(run['id'])))
        temp = await asyncio.gather(*tasks)
        tests.extend(list(itertools.chain.from_iterable(temp)))

    results = []
    test_chunks = split_list_by_chunks(tests, 100)
    for idx, chunk in enumerate(test_chunks):
        print(f'Started processing chunk {idx} of {len(test_chunks)} of tests')
        tasks = []
        for test in chunk:
            tasks.append(asyncio.create_task(testrail_client.get_results(test['id'])))
        results.extend(list(itertools.chain.from_iterable(await asyncio.gather(*tasks))))

    for result in results:
        test_idx = find_idx_by_key_value('id', result['test_id'], tests)
        if not tests[test_idx].get('results'):
            tests[test_idx]['results'] = []
        tests[test_idx]['results'].append(result)

    for test in tests:
        run_idx = find_idx_by_key_value('id', test['run_id'], runs)
        if not runs[run_idx].get('tests'):
            runs[run_idx]['tests'] = []
        runs[run_idx]['tests'].append(test)

    return runs, tests, results


async def get_plans_w_runs(testrail_client, plans_without_runs):
    plans = []
    plan_chunks = split_list_by_chunks(plans_without_runs, 100)
    for idx, chunk in enumerate(plan_chunks):
        print(f'Processing plan chunk {idx} of {len(plan_chunks)}')
        tasks = []
        for plan in chunk:
            tasks.append(testrail_client.get_plan_async(plan['id']))
        plans.extend(await asyncio.gather(*tasks))
    return plans


async def download_representations(testrail_client: TestRailClient, project_id: int):
    with timer('Took time:'):
        milestones = testrail_client.get_milestones(project_id)
        child_miles = {}
        for idx, milestone in enumerate(milestones):
            if milestone.get('milestones'):
                child_miles[idx] = milestone['milestones']
                milestone['milestones'] = []

    plans_without_runs = testrail_client.get_plans(project_id)
    runs_from_plan = []
    with timer('Getting plans took:'):
        plans = await get_plans_w_runs(testrail_client, plans_without_runs)
        for plan in plans:
            for entry in plan['entries']:
                runs_from_plan.extend(entry['runs'])

    # with timer('Getting tests and results for runs without plans took:'):
    #     runs = testrail_client.get_runs(project_id)
    #     runs_without_plans, tests_without_test_plans, results_without_test_plans = await get_tests_results_by_run(
    #         testrail_client, runs)
    # with timer('Getting tests and results for runs from plans'):
    #     runs_with_plan, tests_with_test_plan, results_with_test_plans = await get_tests_results_by_run(testrail_client, runs_from_plan)
    #
    with open('/Users/r.kabaev/Desktop/testrail_migrator/backup/runs_without_plans2022-12-05 01:49:54.279145.json',
              'r') as file:
        runs_without_plans = json.loads(file.read())
    with open('/Users/r.kabaev/Desktop/testrail_migrator/backup/runs_with_plan2022-12-05 01:50:01.598290.json',
              'r') as file:
        runs_with_plan = json.loads(file.read())

    for run in runs_with_plan:
        plan_idx = find_idx_by_key_value('id', run['plan_id'], plans)
        if not plans[plan_idx].get('runs'):
            plans[plan_idx]['runs'] = []
        plans[plan_idx]['runs'].append(run)

    for idx, run in enumerate(runs_without_plans):
        print(f'Adding run without test plan to json {idx} of {len(runs_without_plans)}')
        milestone_id = run.get('milestone_id')

        milestone_idx = find_idx_by_key_value('id', milestone_id, milestones)
        if milestone_idx:
            if not milestones[milestone_idx].get('runs'):
                milestones[milestone_idx]['runs'] = []
            milestones[milestone_idx]['runs'].append(run)
            continue

        for child_mile in child_miles.values():
            milestone_idx = find_idx_by_key_value('id', milestone_id, child_mile)
            if not milestone_idx:
                continue
            if not child_mile[milestone_idx].get('runs'):
                child_mile[milestone_idx]['runs'] = []
            child_mile[milestone_idx]['runs'].append(run)

    for idx, plan in enumerate(plans):
        print(f'Adding run with test plan to json {idx} of {len(plans)}')
        milestone_id = plan.get('milestone_id')
        milestone_idx = find_idx_by_key_value('id', milestone_id, milestones)
        if milestone_idx:
            if not milestones[milestone_idx].get('plans'):
                milestones[milestone_idx]['plans'] = []
            milestones[milestone_idx]['plans'].append(plan)
            continue
        for child_mile in child_miles.values():
            milestone_idx = find_idx_by_key_value('id', milestone_id, milestones)
            if not milestone_idx:
                continue
            if not child_mile[milestone_idx].get('plans'):
                child_mile[milestone_idx]['plans'] = []
            child_mile[milestone_idx]['plans'].append(plan)

    for mile_idx, child_mile in child_miles.items():
        milestones[mile_idx]['milestones'] = child_mile

    # with open(f'/Users/r.kabaev/Desktop/testrail_migrator/backup/resulting{datetime.now()}.json', 'w') as file:
    #     file.write(json.dumps(milestones, indent=2))

    # name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_test_plans')
    # parameters = ArrayField(models.PositiveIntegerField(null=True, blank=True), null=True, blank=True)
    # started_at = models.DateTimeField()
    # due_date = models.DateTimeField()
    # finished_at = models.DateTimeField(null=True, blank=True)
    # is_archive = models.BooleanField(default=False)
    # TODO: add description field to TestPlan
    # TODO: rename milestones to tree
    return plans, runs_with_plan, runs_without_plans, milestones


async def create_milestones_via_endpoint(testy_client, milestones, project_id):
    milestones_mapping = {}
    tasks = []
    milestones_bar = tqdm(milestones)
    milestones_bar.set_description('Parent milestones progress')
    for milestone in milestones_bar:
        milestone_data = {
            'project': project_id,
            'name': milestone['name'],
            'is_archive': milestone['is_completed'],
            'started_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(milestone['started_on'])),
            'finished_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(milestone['completed_on'])),
            'due_date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(milestone['due_on']))
        }
        tasks.append(
            asyncio.create_task(
                testy_client.create_plan_async(milestone_data, milestone['id'])
            )
        )
    for mapping in await asyncio.gather(*tasks):
        milestones_mapping.update(mapping)
    tasks.clear()

    milestones_bar = tqdm(milestones)
    milestones_bar.set_description('Parent milestones progress')
    for milestone in milestones_bar:
        if not milestone['milestones']:
            continue
        child_milestone_bar = tqdm(milestone['milestones'])
        child_milestone_bar.set_description('Child milestones progress')
        for child_milestone in child_milestone_bar:
            milestone_data = {
                'project': project_id,
                'name': child_milestone['name'],
                'is_archive': child_milestone['is_completed'],
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(milestone['started_on'])),
                'finished_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(child_milestone['completed_on'])),
                'due_date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(child_milestone['due_on'])),
                'parent': milestones_mapping[milestone['id']]
            }
            tasks.append(
                asyncio.create_task(
                    testy_client.create_plan_async(milestone_data, child_milestone['id'])
                )
            )

    for mapping in await asyncio.gather(*tasks):
        milestones_mapping.update(mapping)
    tasks.clear()

    return milestones_mapping


def create_milestones(milestones, project_id):
    milestones_mapping = {}
    parent_milestones = []
    for milestone in milestones:
        milestone_data = {
            'project': project_id,
            'name': milestone['name'],
            'is_archive': milestone['is_completed'],
            'started_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(milestone['started_on'])),
            'finished_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(milestone['completed_on'])),
            'due_date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(milestone['due_on']))
        }
        parent_milestones.append(milestone_data)

    serializer = TestPlanInputSerializer(data=parent_milestones, many=True)
    serializer.is_valid(raise_exception=True)
    test_plans = TestPLanService().testplan_bulk_create(serializer.validated_data)
    for tr_milestone, testy_milestone in zip(milestones, test_plans):
        milestones_mapping.update({tr_milestone['id']: testy_milestone.id})

    for milestone in milestones:
        if not milestone['milestones']:
            continue
        child_milestones_data_list = []
        for child_milestone in milestone['milestones']:
            milestone_data = {
                'project': project_id,
                'name': child_milestone['name'],
                'is_archive': child_milestone['is_completed'],
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(milestone['started_on'])),
                'finished_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(child_milestone['completed_on'])),
                'due_date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(child_milestone['due_on'])),
                'parent': milestones_mapping[milestone['id']]
            }
            child_milestones_data_list.append(milestone_data)

        serializer = TestPlanInputSerializer(data=child_milestones_data_list, many=True)
        serializer.is_valid(raise_exception=True)
        test_plans = TestPLanService().testplan_bulk_create(serializer.validated_data)

        for tr_milestone, testy_milestone in zip(milestone['milestones'], test_plans):
            milestones_mapping.update({tr_milestone['id']: testy_milestone.id})

    return milestones_mapping


async def create_plans_via_endpoint(testy_client: TestyClient, plans, milestones_mappings, project_id,
                                    map_to_plan: bool = False):
    tasks = []
    plan_data_list = []
    plan_mappings = {}
    for plan in plans:
        mapping_id = plan['plan_id' if map_to_plan else 'milestone_id']
        due_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(plan.get('due_on')))
        if not plan.get('due_on'):
            due_date = (datetime.now() + relativedelta(years=5, days=5)).strftime('%Y-%m-%d %H:%M:%S')
        plan_data = {
            'project': project_id,
            'name': plan['name'],
            'is_archive': plan['is_completed'],
            'started_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(plan['created_on'])),
            'finished_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(plan['completed_on'])),
            'due_date': due_date,
        }
        if mapping_id:
            plan_data['parent'] = milestones_mappings[mapping_id]
        plan_data_list.append(plan_data)

    serializer = TestPlanInputSerializer(data=plan_data_list, many=True)
    serializer.is_valid(raise_exception=True)
    test_plans = TestPLanService().testplan_bulk_create(serializer.validated_data)
    print()
    # for src_plan, created_plan in zip(chunk, created_plans):
    #     plan_mappings[src_plan['id']] = created_plan['id']
    #     tasks.append(
    #         asyncio.create_task(
    #             testy_client.create_plan_async(plan_data, plan['id'])
    #         )
    #     )
    # for mapping in await asyncio.gather(*tasks):
    #     plan_mappings.update(mapping)

    return plan_mappings


async def create_tests_via_endpoint(testy_client: TestyClient, tests, plans_mappings, project_id):
    tasks = []
    tests_mappings = {}
    for test in tests:
        test_data = {
            'project': project_id,
            'name': test['name'],
            'is_archive': test['is_completed'],
            'finished_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(test['completed_on'])),
            'due_date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(test['due_on'])),
            'parent': plans_mappings[test['run_id']]
        }
        tasks.append(
            asyncio.create_task(
                testy_client.create_test_async(test_data, test['id'])
            )
        )

    for mapping in await asyncio.gather(*tasks):
        tests_mappings.update(mapping)

    return tests_mappings


#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     status = models.IntegerField(choices=TestStatuses.choices, default=TestStatuses.UNTESTED)
#     test = models.ForeignKey(Test, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     comment = models.TextField(blank=True)
#     is_archive = models.BooleanField(default=False)


async def create_results_via_endpoint(testy_client: TestyClient, results, tests_mappings, project_id):
    statuses = {
        1: 1,  # passed
        5: 0,  # failed
        8: 2,  # skipped
        2: 4,  # Retest
        3: 5,  # Untested
        4: 3  # Not matching retest in tr / broken in testy
    }
    tasks = []
    results_mappings = {}
    for result in results:
        result_dict = {
            'project': project_id,
            'status': statuses.get(result['status_id']),
            'comment': result['comment'],
            'test': tests_mappings[result['test_id']],
            'test_case_version': result['version']
        }
        tasks.append(
            asyncio.create_task(
                testy_client.create_result_async(result_dict, result['id'])
            )
        )

    for mapping in await asyncio.gather(*tasks):
        results_mappings.update(mapping)

    return results_mappings


async def main():
    # args = parse_args()
    testrail_client, testy_client = init_tms_clients('/Users/r.kabaev/Desktop/testrail_migrator/config.yaml')

    # Descriptions

    # Testrail part
    # suites_and_cases = get_suites_cases_from_tr(testrail_client, args.dump_filepath, from_dump=True)
    # Testy part
    # with timer('Uploading tests'):
    #     case_mappings = await upload_suites_cases_to_testy(testy_client)
    #     with open(f'/Users/r.kabaev/Desktop/testrail_migrator/backup_suites_cases/case_mappings{datetime.now()}.json','w') as file:
    #         file.write(json.dumps(case_mappings, indent=2))

    # Representations
    # Testrail part
    with timer('Download representations'):
        milestones = testrail_client.get_milestones(1)
        plans_without_runs = testrail_client.get_plans(1)
        runs_from_plan = []
        with timer('Getting plans took:'):
            plans = await get_plans_w_runs(testrail_client, plans_without_runs)
            for plan in plans:
                for entry in plan['entries']:
                    runs_from_plan.extend(entry['runs'])
        # plans, runs_with_plan, runs_without_plans, milestones = await download_representations(testrail_client, project_id=1)

    with open(
            f'/Users/r.kabaev/Desktop/testrail_migrator/temp_backup/milestones2022-12-06 16:36:14.618443.json',
            'r') as file:
        milestones = json.loads(file.read())

    with open(
            f'/Users/r.kabaev/Desktop/testrail_migrator/temp_backup/results_with_test_plans2022-12-05 20:38:57.790758.json',
            'r') as file:
        results_with_test_plans = json.loads(file.read())
    with open(
            f'/Users/r.kabaev/Desktop/testrail_migrator/temp_backup/results_without_test_plans2022-12-05 20:36:59.781118.json',
            'r') as file:
        results_without_test_plans = json.loads(file.read())
    with open(f'/Users/r.kabaev/Desktop/testrail_migrator/temp_backup/runs_with_plan2022-12-05 20:37:01.498579.json',
              'r') as file:
        runs_with_plans = json.loads(file.read())
    with open(
            f'/Users/r.kabaev/Desktop/testrail_migrator/temp_backup/runs_without_plans2022-12-05 20:36:49.323261.json',
            'r') as file:
        runs_without_plans = json.loads(file.read())
    with open(
            f'/Users/r.kabaev/Desktop/testrail_migrator/temp_backup/tests_with_test_plan2022-12-05 20:38:12.798847.json',
            'r') as file:
        tests_with_test_plan = json.loads(file.read())
    with open(
            f'/Users/r.kabaev/Desktop/testrail_migrator/temp_backup/tests_without_test_plans2022-12-05 20:36:55.567101.json',
            'r') as file:
        tests_without_test_plans = json.loads(file.read())

    # testy_client.create_project({'name': 'Tatlin'})
    # await sync_to_async(Project.objects.create)(**{'name': 'Tatlin'})
    # milestones_mappings = await create_milestones_via_endpoint(testy_client, milestones, project_id=1)
    milestones_mappings = create_milestones(milestones, project_id=1)
    testplan_mappings = await create_plans_via_endpoint(testy_client, plans, milestones_mappings, project_id=1)
    # runs_without_plans_mappings = await create_plans(testy_client, runs_without_plans, milestones_mappings,
    #                                                  project_id=1)
    # runs_with_plans_mappings = await create_plans(testy_client, runs_with_plans, testplan_mappings, project_id=1,
    #                                               map_to_plan=True)
    # tests_with_test_plan_mappings = await create_tests(testy_client, tests_with_test_plan, runs_with_plans_mappings,
    #                                                    project_id=1)
    # tests_without_test_plan_mappings = await create_tests(testy_client, tests_without_test_plans,
    #                                                       runs_without_plans_mappings, project_id=1)
    # await create_results(testy_client, results_with_test_plans, tests_with_test_plan_mappings, project_id=1)
    # await create_results(testy_client, results_without_test_plans, tests_without_test_plan_mappings, project_id=1)


#     serializer = TestPlanInputSerializer(data=plan_data_list, many=True)
#     serializer.is_valid(raise_exception=True)
#     test_plans = TestPLanService().testplan_bulk_create(serializer.validated_data)
def create_cases_suites(suites_cases, project_id):
    cases_mappings = {}
    for suite in suites_cases:
        suite_data = {
            'name': suite['name'],
            'project': project_id,
        }
        serializer = TestSuiteSerializer(data=suite_data)
        serializer.is_valid(raise_exception=True)
        created_suite = TestSuiteService().suite_create(serializer.validated_data)
        cases_data_list = []
        for case in suite['cases']:
            case_data = {
                'name': case['title'],
                'project': project_id,
                'suite': created_suite.id,
                'scenario': case['custom_steps'],
            }
            cases_data_list.append(case_data)
        serializer = TestCaseSerializer(data=cases_data_list, many=True)
        serializer.is_valid(raise_exception=True)
        created_cases = TestCaseService().cases_bulk_create(serializer.validated_data)
        for tr_case, case in zip(suite['cases'], created_cases):
            cases_mappings.update({tr_case['id']: case.id})
    return cases_mappings


def create_configs(config_groups, project_id):
    parameters_mappings = {}
    parameter_data_list = []
    src_config_ids = []
    for config_group in config_groups:
        for config in config_group['configs']:
            src_config_ids.append(config['id'])
            parameter_data = {
                'group_name': config_group['name'],
                'data': config['name'],
                'project': project_id,
            }
            parameter_data_list.append(parameter_data)

    serializer = ParameterSerializer(data=parameter_data_list, many=True)
    serializer.is_valid(raise_exception=True)
    created_parameters = ParameterService().parameter_bulk_create(serializer.validated_data)
    for tr_config_id, testy_parameter in zip(src_config_ids, created_parameters):
        parameters_mappings.update({tr_config_id: testy_parameter.id})

    return parameters_mappings


def create_plans(plans, milestones_mappings, project_id, skip_root_plans: bool = True):
    plan_data_list = []
    plan_mappings = {}
    for plan in plans:
        mapping_id = plan['milestone_id']
        due_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(plan.get('due_on')))
        if not plan.get('due_on'):
            due_date = (datetime.now() + relativedelta(years=5, days=5)).strftime('%Y-%m-%d %H:%M:%S')
        plan_data = {
            'project': project_id,
            'name': plan['name'],
            'is_archive': plan['is_completed'],
            'started_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(plan['created_on'])),
            'finished_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(plan['completed_on'])),
            'due_date': due_date,
        }
        if not mapping_id and skip_root_plans:
            continue
        if mapping_id:
            plan_data['parent'] = milestones_mappings[mapping_id]
        plan_data_list.append(plan_data)

    serializer = TestPlanInputSerializer(data=plan_data_list, many=True)
    serializer.is_valid(raise_exception=True)
    test_plans = TestPLanService().testplan_bulk_create(serializer.validated_data)
    for tr_milestone, testy_milestone in zip(plans, test_plans):
        plan_mappings.update({tr_milestone['id']: testy_milestone.id})

    return plan_mappings


def create_runs_parent_plan(runs, plan_mappings, config_mappings, tests, case_mappings, project_id):
    #     name = models.CharField(max_length=settings.CHAR_FIELD_MAX_LEN)
    #     project = models.ForeignKey(Project, on_delete=models.CASCADE)
    #     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_test_plans')
    #     parameters = ArrayField(models.PositiveIntegerField(null=True, blank=True), null=True, blank=True)
    #     started_at = models.DateTimeField()
    #     due_date = models.DateTimeField()
    #     finished_at = models.DateTimeField(null=True, blank=True)
    #     is_archive = models.BooleanField(default=False)
    #     test_cases = PrimaryKeyRelatedField(queryset=TestCaseSelector().case_list(), many=True, required=False)
    #     parameters
    run_data_list = []
    tests_mappings = {}
    src_tests = []
    for idx, run in enumerate(runs, start=1):
        parent = plan_mappings.get(run['plan_id'])
        if not parent:
            continue
        tests_for_run = [test for test in tests if test['run_id'] == run['id']]
        src_tests.extend(tests_for_run)
        cases = [case_mappings[test['case_id']] for test in tests_for_run]
        parameters = [config_mappings[config_id] for config_id in run['config_ids']]
        due_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(run.get('due_on')))
        if not run.get('due_on'):
            due_date = (datetime.now() + relativedelta(years=5, days=5)).strftime('%Y-%m-%d %H:%M:%S')
        run_data = {
            'project': project_id,
            'name': run['name'],
            'started_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(run['created_on'])),
            'due_date': due_date,
            'parent': parent,
            'test_cases': cases,
            'parameters': parameters
        }
        run_data_list.append(run_data)
    serializer = TestPlanInputSerializer(data=run_data_list, many=True)
    serializer.is_valid(raise_exception=True)
    created_tests = TestPLanService().testplan_bulk_create_with_tests(serializer.validated_data)
    return dict(zip(
        [src_test['id'] for src_test in src_tests],
        [created_test.id for created_test in created_tests])
    )


def create_tests(tests, case_mappings, plans_mappings, project_id):
    test_data_list = []
    tests_mappings = {}
    for test in tests:
        if not case_mappings.get(test['case_id']) or not plans_mappings.get(test['run_id']):
            continue
        test_data = {
            'project': project_id,
            'case': case_mappings[test['case_id']],
            'plan': plans_mappings[test['run_id']]
        }
        test_data_list.append(test_data)
    serializer = TestSerializer(data=test_data_list, many=True)
    serializer.is_valid(raise_exception=True)
    created_tests = TestService().tests_bulk_create_by_data_list(serializer.validated_data)
    for tr_test, testy_test in zip(tests, created_tests):
        tests_mappings.update({tr_test['id']: testy_test.id})

    return tests_mappings


def create_results(results, tests_mappings, user):
    statuses = {
        1: 1,  # passed
        5: 0,  # failed
        8: 2,  # skipped
        2: 4,  # Retest
        3: 5,  # Untested
        4: 3  # Not matching retest in tr / broken in testy
    }
    results_data_list = []
    created_results = []
    for idx, result in enumerate(results):
        print(f'Processing result {idx} of {len(results)}')
        if not tests_mappings.get(result['test_id']):
            continue
        result_data = {
            'status': statuses.get(result['status_id'], 5),
            'comment': result['comment'],
            'test': tests_mappings[result['test_id']],
        }
        serializer = TestResultSerializer(data=result_data)
        serializer.is_valid(raise_exception=True)
        created_results.append(TestResultService().result_create(serializer.validated_data, user))
    #     results_data_list.append(result_data)
    # serializer = TestResultSerializer(data=results_data_list, many=True)
    # serializer.is_valid(raise_exception=True)
    # created_results = TestResultService().create_bulk_results(serializer.validated_data)
    return created_results


def upload_to_testy(project_id, user):
    try:
        with open(
                f'/Users/r.kabaev/Desktop/testrail_migrator/backup_suites_cases/resulting2022-12-05 13:59:13.870764.json',
                'r') as file:
            suites_cases = json.loads(file.read())

        with open(f'/Users/r.kabaev/Desktop/testrail_migrator/backup_08.12/backup2022-12-08 01:08:34.356653.json',
                  'r') as file:
            backup = json.loads(file.read())

        configs = backup['configs']
        milestones = backup['milestones']
        plans = backup['plans']
        runs_parent_plan = backup['runs_parent_plan']
        tests_parent_plan = backup['tests_parent_plan']
        results_parent_plan = backup['results_parent_plan']
        #     results_without_test_plans = json.loads(file.read())
        #     runs_without_plans = json.loads(file.read())
        #     tests_without_test_plans = json.loads(file.read())

        config_mappings = create_configs(configs, project_id)
        print('Configs finished')
        cases_mappings = create_cases_suites(suites_cases['suites'], project_id)
        print('Cases finished')
        milestones_mappings = create_milestones(milestones, project_id)  # Milestones are working
        print('milestones_mappings finished')
        plans_mappings = create_plans(plans, milestones_mappings, project_id)
        print('plans_mappings finished')
        test_mappings = create_runs_parent_plan(
            runs=runs_parent_plan,
            plan_mappings=plans_mappings,
            config_mappings=config_mappings,
            tests=tests_parent_plan,
            case_mappings=cases_mappings,
            project_id=project_id
        )
        create_results(results_parent_plan, test_mappings, user)
        print('runs_parent_plan_mappings finished')
    except Exception as err:
        logging.error(str(err))
        raise err

    # print('all finished')
    # return
# 28053
