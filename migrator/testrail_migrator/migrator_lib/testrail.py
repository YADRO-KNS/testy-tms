import asyncio
import itertools
import logging

import aiohttp
from aiohttp import ClientConnectionError
from tqdm.asyncio import tqdm

from .config import TestrailConfig
from .utils import split_list_by_chunks, timer


# TODO: вынести значение размера чанка в конфиг
class TestRailClientError(Exception):
    """Raise if error in this module happens."""

    def __init__(self, msg):
        """
        logger an error as critical if it occurred.

        Args:
            msg: error message
        """
        # logger.critical(str(msg))
        super().__init__(msg)


class TestRailClient:
    """Implement testrail client."""

    def __init__(self, config: TestrailConfig):
        """
        Init method for TestRailClient.

        Args:
            config: instance of TestrailConfig
        """
        if not config.login or not config.password:
            raise TestRailClientError('No login or password were provided.')
        self.config = config
        self.session = aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.config.login, self.config.password))

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def download_descriptions(self, project_id: int):
        descriptions_dict = {}
        with timer('Getting suites'):
            descriptions_dict['suites'] = await self.get_suites(project_id)

        with timer('Getting cases'):
            descriptions_dict['cases'] = await self.get_cases(project_id, descriptions_dict['suites'])

        return descriptions_dict

    async def download_representations(self, project_id: int):
        representations_dict = {}
        with timer('Getting configs'):
            configs = await self.get_configs(project_id)
            representations_dict['configs'] = configs

        with timer('Getting miles'):
            milestones = await self.get_milestones(project_id, query_params={'is_completed': 0})
            for milestone in milestones:
                filtered_children = [child_milestone for child_milestone in milestone['milestones'] if
                                     not child_milestone['is_completed']]
                milestone['milestones'] = filtered_children

            representations_dict['milestones'] = milestones

        plans_list = await self.get_plans(project_id, query_params={'is_completed': 0})
        representations_dict['plans'] = await self.get_plans_with_runs(plans_list)

        runs_parent_plan = []
        for plan in representations_dict['plans']:
            for entry in plan['entries']:
                runs_parent_plan.extend(entry['runs'])
        representations_dict['runs_parent_plan'] = runs_parent_plan

        with timer('Getting runs with milestone as parent'):
            representations_dict['runs_parent_mile'] = await self.get_runs(project_id, query_params={'is_completed': 0})

        representations_dict['tests_parent_plan'] = await self.get_tests_for_runs(runs_parent_plan)

        representations_dict['tests_parent_mile'] = await self.get_tests_for_runs(
            representations_dict['runs_parent_mile']
        )

        representations_dict['results_parent_plan'] = await self.get_results_for_tests(
            representations_dict['tests_parent_plan']
        )

        representations_dict['results_parent_mile'] = await self.get_results_for_tests(
            representations_dict['tests_parent_mile']
        )
        return representations_dict

    async def get_plans_with_runs(self, plans_without_runs):
        plans = []
        plan_chunks = split_list_by_chunks(plans_without_runs)
        for chunk in tqdm(plan_chunks, desc='Plans progress'):
            tasks = []
            for plan in chunk:
                tasks.append(self.get_plan(plan['id']))
            plans.extend(await tqdm.gather(*tasks, desc='Plans chunk progress', leave=False))
        return plans

    async def get_results_for_tests(self, tests):
        results = []
        test_chunks = split_list_by_chunks(tests)
        for chunk in tqdm(test_chunks, desc='Getting results for tests'):
            tasks = []
            for test in chunk:
                tasks.append(self.get_results(test['id']))
            results.extend(
                list(
                    itertools.chain.from_iterable(await tqdm.gather(*tasks, desc='Results chunk progress', leave=False))
                )
            )
        return results

    async def get_tests_for_runs(self, runs):
        tests = []
        run_chunks = split_list_by_chunks(runs)
        for chunk in tqdm(run_chunks, desc='Getting tests for runs'):
            tasks = []
            for run in chunk:
                tasks.append(self.get_tests(run['id']))
            tests.extend(
                list(itertools.chain.from_iterable(await tqdm.gather(*tasks, desc='Tests chunk progress', leave=False)))
            )
        return tests

    async def get_suites(self, project_id):
        return await self._process_request(f'/get_suites/{project_id}')

    async def get_project(self, project_id):
        return await self._process_request(f'/get_project/{project_id}')

    async def get_cases_for_suite(self, project_id, suite_id):
        return await self._process_request(f'/get_cases/{project_id}', query_params={'suite_id': suite_id})

    async def get_cases(self, project_id, suites):
        tests = []
        suite_chunks = split_list_by_chunks(suites)
        for chunk in tqdm(suite_chunks, desc='Getting cases for suites'):
            tasks = []
            for suite in chunk:
                tasks.append(self.get_cases_for_suite(project_id, suite['id']))
            tests.extend(
                list(itertools.chain.from_iterable(await tqdm.gather(*tasks, desc='Cases chunk progress', leave=False)))
            )
        return tests

    async def get_milestones(self, project_id: int, query_params=None):
        return await self._process_request(f'/get_milestones/{project_id}', query_params=query_params)

    async def get_configs(self, project_id):
        return await self._process_request(f'/get_configs/{project_id}')

    async def get_plans(self, project_id: int, query_params=None):
        return await self._process_request(f'/get_plans/{project_id}', query_params=query_params)

    async def get_runs(self, project_id: int, query_params=None):
        return await self._process_request(f'/get_runs/{project_id}', query_params=query_params)

    async def get_plan(self, plan_id):
        return await self._process_request(f'/get_plan/{plan_id}')

    async def get_tests(self, run_id: int):
        return await self._process_request(f'/get_tests/{run_id}')

    async def get_results(self, test_id: int):
        return await self._process_request(f'/get_results/{test_id}')

    async def _process_request(
            self, endpoint: str,
            headers=None,
            query_params=None,
            retry_count: int = 30
    ):
        if not headers:
            headers = {
                'Content-Type': 'application/json; charset=utf-8'
            }
        url = self.config.api_url + endpoint

        if query_params:
            url = f'{url}&{"&".join([f"{field}={field_value}" for field, field_value in query_params.items()])}'

        while retry_count:
            try:
                async with self.session.get(url=url, headers=headers) as resp:
                    response = await resp.json()
                    if resp.status != 200:
                        logging.error(response)
                        raise ClientConnectionError
                    return response
            except (ClientConnectionError, asyncio.TimeoutError):
                retry_count -= 1
