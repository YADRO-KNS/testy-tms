import argparse
import asyncio
import itertools
import json
import time
from contextlib import contextmanager
from datetime import datetime
from typing import Any

from migrator_lib import TestRailClient, TestrailConfig, TestyClient, TestyConfig, parse_yaml_config
from tqdm import tqdm


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
            tasks = []
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


async def create_milestones(testy_client, milestones, project_id):
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


async def create_plans(testy_client: TestyClient, plans, milestones_mappings, project_id, map_to_plan: bool = False):
    tasks = []
    plan_mappings = {}
    for plan in plans:
        plan_data = {
            'project': project_id,
            'name': plan['name'],
            'is_archive': plan['is_completed'],
            'finished_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(plan['completed_on'])),
            'due_date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(plan['due_on'])),
            'parent': milestones_mappings[plan['plan_id' if map_to_plan else 'milestone_id']]
        }
        tasks.append(
            asyncio.create_task(
                testy_client.create_plan_async(plan_data, plan['id'])
            )
        )

    for mapping in await asyncio.gather(*tasks):
        plan_mappings.update(mapping)

    return plan_mappings


async def create_tests(testy_client: TestyClient, tests, plans_mappings, project_id):
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


async def create_results(testy_client: TestyClient, results, tests_mappings, project_id):
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
    args = parse_args()
    testrail_client, testy_client = init_tms_clients(args.config_path)

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
        plans, runs_with_plan, runs_without_plans, milestones = await download_representations(testrail_client,
                                                                                               project_id=1)
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

    milestones_mappings = await create_milestones(testy_client, milestones, project_id=1)
    testplan_mappings = await create_plans(testy_client, plans, milestones_mappings, project_id=1)
    runs_without_plans_mappings = await create_plans(testy_client, runs_without_plans, milestones_mappings,
                                                     project_id=1)
    runs_with_plans_mappings = await create_plans(testy_client, runs_with_plans, testplan_mappings, project_id=1,
                                                  map_to_plan=True)
    tests_with_test_plan_mappings = await create_tests(testy_client, tests_with_test_plan, runs_with_plans_mappings,
                                                       project_id=1)
    tests_without_test_plan_mappings = await create_tests(testy_client, tests_without_test_plans,
                                                          runs_without_plans_mappings, project_id=1)
    await create_results(testy_client, results_with_test_plans, tests_with_test_plan_mappings, project_id=1)
    await create_results(testy_client, results_without_test_plans, tests_without_test_plan_mappings, project_id=1)


if __name__ == '__main__':
    asyncio.run(main())
