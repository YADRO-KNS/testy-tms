import asyncio
import json
from copy import deepcopy
from http import HTTPStatus
from typing import Union

import aiohttp
import requests
import urllib3
from aiohttp import ClientConnectionError
from requests.adapters import HTTPAdapter

from .config import TestrailConfig


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
        urllib3.disable_warnings()
        self._auth = (config.login, config.password)
        if not config.login or not config.password:
            raise TestRailClientError('No login or password were provided.')
        self.config = config

    def get_projects(self):
        return self._process_request('/get_projects/')

    def get_suites(self, project_id):
        return self._process_request(f'/get_suites/{project_id}')

    def get_project(self, project_id):
        return self._process_request(f'/get_project/{project_id}')

    def get_cases(self, project_id, suite_id):
        # TODO: add logger
        print(f'get cases for project "{project_id}" and suite "{suite_id}"')
        return self._process_request(f'/get_cases/{project_id}&suite_id={suite_id}')

    def get_attachments(self, case_id):
        print(f'get attachments for case "{case_id}"')
        return self._process_request(f'/get_attachments_for_case/{case_id}')

    def get_suites_cases_for_project(self, project_id):
        project = self.get_project(project_id)
        project['suites'] = self.get_suites(project['id'])
        for suite in project['suites']:
            suite['cases'] = self.get_cases(project['id'], suite['id'])
        return deepcopy(project)

    def get_case(self, case_id):
        return self._process_request(f'/get_case/{case_id}')

    def get_all_for_all_projects(self):
        result = []
        for project in self.get_projects():
            result.append(self.get_suites_cases_attachments_for_project(project))
        num_suites = 0
        num_cases = 0
        for pr in result:
            num_suites += len(pr['suites'])
            num_cases += len(pr['suites']['cases'])
        print('number of suites', num_suites)
        print('number of cases', num_cases)
        return result

    # def get_suites_cases_for_single_project(self, project_id):
    #     project =
    #     num_suites = 0
    #     num_cases = 0
    #     num_suites += len(project['suites'])
    #     for suite in project['suites']:
    #         num_cases += len(suite['cases'])
    #     print('number of suites', num_suites)
    #     print('number of cases', num_cases)
    #     return project
    #
    #     # 328

    def get_milestones(self, project_id: int, query_params=None):
        return self._process_request(f'/get_milestones/{project_id}', query_params=query_params)

    def get_configs(self, project_id):
        return self._process_request(f'/get_configs/{project_id}')

    def get_milestone(self, milestone_id: int):
        return self._process_request(f'/get_milestone/{milestone_id}')

    def get_plans(self, project_id: int, query_params=None):
        return self._process_request(f'/get_plans/{project_id}', query_params=query_params)

    # async def get_plans_with_runs(self, plans_without_runs):
    #     tasks = []
    #
    #     async with aiohttp.ClientSession(
    #             auth=aiohttp.BasicAuth(self.config.login, self.config.password)
    #     ) as session:
    #         for plan in plans_without_runs:
    #             tasks.append(self.get_plan_async(plan['id'], session))
    #         plans = await asyncio.gather(*tasks)
    #         return plans

    # async def get_plans_with_runs(self, plans_without_runs):
    #     tasks = []
    #     async with aiohttp.ClientSession(
    #             auth=aiohttp.BasicAuth(self.config.login, self.config.password)
    #     ) as session:
    #         for plan in plans_without_runs:
    #             tasks.append(self.get_plan_async(plan['id'], session))
    #         return await asyncio.gather(*tasks)

    def get_plan(self, plan_id: int):
        return self._process_request(f'/get_plan/{plan_id}')

    def get_runs(self, project_id: int, query_params=None):
        return self._process_request(f'/get_runs/{project_id}', query_params=query_params)

    def get_run(self, run_id: int):
        return self._process_request(f'/get_run/{run_id}')

    async def get_plan_async(self, plan_id):
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.config.login, self.config.password)) as session:
            return await self._process_async_request(f'/get_plan/{plan_id}', session=session)

    async def get_tests(self, run_id: int):
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.config.login, self.config.password)) as session:
            return await self._process_async_request(f'/get_tests/{run_id}', session=session)

    async def get_results(self, test_id: int):
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.config.login, self.config.password)) as session:
            return await self._process_async_request(f'/get_results/{test_id}', session=session)

    def _process_request(self, endpoint: str, input_data=None, headers=None, query_params=None) -> Union[
        list, dict, None]:
        """
        Process request to TestRail REST API.

        Args:
            endpoint: endpoint url
            input_data: content

        Returns:
            data or None for error
        """
        session = requests.Session()
        retries = urllib3.Retry(total=200, backoff_factor=0.1)
        session.mount('https://', HTTPAdapter(max_retries=retries))
        if not headers:
            headers = {
                'Content-Type': 'application/json; charset=utf-8'
            }
        url = self.config.api_url + endpoint
        if query_params:
            url = f'{url}&{"&".join([f"{field}={field_value}" for field, field_value in query_params.items()])}'

        if input_data:
            # logger.debug(f'Request POST - {endpoint}, data: {input_data}')
            response = requests.post(url, json=input_data, auth=self._auth, headers=headers)
        else:
            # logger.debug(f'Request GET - {endpoint}')
            response = session.get(url, auth=self._auth, headers=headers)
        received = json.loads(response.content)
        if response.status_code == HTTPStatus.OK:
            # logger.debug(f'Response ok - {received}')
            return received
        else:
            # logger.warning(f'Response error - status code {response.status_code}, {response.content.decode()}')
            pass

    async def _process_async_request(self, endpoint: str, input_data=None, session=None, headers=None,
                                     retry_count: int = 30):
        # session = requests.Session()
        # retries = urllib3.Retry(total=200, backoff_factor=0.1)
        # session.mount('https://', HTTPAdapter(max_retries=retries))
        if not headers:
            headers = {
                'Content-Type': 'application/json; charset=utf-8'
            }
        url = self.config.api_url + endpoint

        while retry_count:
            try:
                async with session.get(url=url, headers=headers) as resp:
                    response = await resp.json()
                    if resp.status != 200:
                        raise ClientConnectionError
                    return response
            except ClientConnectionError:
                retry_count -= 1


