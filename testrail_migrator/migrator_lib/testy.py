import json
from typing import Union

import aiohttp
import requests
import urllib3
from aiohttp import ClientConnectionError
from requests.adapters import HTTPAdapter

from .config import TestyConfig

testrail_to_testy_mapping = {
    'is_completed': 'is_archive'
}


class TestyClientError(Exception):
    """Raise if error in this module happens."""

    def __init__(self, msg):
        """
        logger an error as critical if it occurred.

        Args:
            msg: error message
        """
        # logger.critical(str(msg))
        super().__init__(msg)


class TestyClient:
    def __init__(self, config: TestyConfig):
        """
        Init method for TestRailClient.

        Args:
            config: instance of TestrailConfig
        """
        urllib3.disable_warnings()
        self._auth = (config.login, config.password)
        if not config.login or not config.password:
            raise TestyClientError('No login or password were provided.')
        self.session = requests.session()
        self.session.mount('http://', HTTPAdapter(max_retries=urllib3.Retry(total=200, backoff_factor=0.1)))
        self.config = config
        with open(config.dumpfile_path, 'r') as file:
            self.dumpfile = json.loads(file.read())

    def create_project(self, project):
        return self._process_request('/projects/', input_data=project)

    def create_suite(self, suite):
        return self._process_request('/suites/', input_data=suite)

    async def create_suite_async(self, suite):
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.config.login, self.config.password)) as session:
            return await self._process_async_request('/suites/', input_data=suite, session=session)

    async def create_case_async(self, case, tr_case_id):
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.config.login, self.config.password)) as session:
            return {
                'tr_case_id': tr_case_id,
                'tt_case': await self._process_async_request('/cases/', input_data=case, session=session)
            }

    async def create_plan_async(self, plan, tr_instance_id):
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.config.login, self.config.password)) as session:
            test_plan = await self._process_async_request('/testplans/', input_data=plan, session=session)
        return {
            tr_instance_id: test_plan[0].get('id')
        }

    async def create_test_async(self, test, tr_instance_id):
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.config.login, self.config.password)) as session:
            test = await self._process_async_request('/tests/', input_data=test, session=session)
        return {
            tr_instance_id: test.get('id')
        }

    async def create_result_async(self, result, tr_instance_id):
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.config.login, self.config.password)) as session:
            test_result = await self._process_async_request('/results/', input_data=result, session=session)
        return {
            tr_instance_id: test_result.get('id')
        }

    def create_case(self, case, tr_case):
        return {tr_case: self._process_request('/cases/', input_data=case)}

    def create_plan(self, plan):
        return self._process_request('/plans/', input_data=plan)

    def _process_request(self, endpoint: str, input_data=None, headers=None) -> Union[list, dict, None]:
        """
        Process request to TestRail REST API.

        Args:
            endpoint: endpoint url
            input_data: content

        Returns:
            data or None for error
        """

        if not headers:
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
            }
        url = self.config.api_url + endpoint
        if input_data:
            # logger.debug(f'Request POST - {endpoint}, data: {input_data}')
            response = self.session.post(url, json=input_data, auth=self._auth, headers=headers)
        else:
            # logger.debug(f'Request GET - {endpoint}')
            response = self.session.get(url, headers=headers, auth=self._auth)
        received = json.loads(response.content)
        # logger.debug(f'Response ok - {received}')
        return received

    async def _process_async_request(self, endpoint: str, input_data=None, session=None, headers=None,
                                     retry_count: int = 30):
        if not headers:
            headers = {
                'Content-Type': 'application/json; charset=utf-8'
            }
        url = self.config.api_url + endpoint

        while retry_count:
            try:
                if input_data:
                    input_data = json.dumps(input_data)
                    async with session.post(url=url, data=input_data, headers=headers) as resp:
                        response = await resp.json()
                        if resp.status not in [200, 201]:
                            print('response:', response, 'input_data:', json.loads(input_data))
                            raise ClientConnectionError
                        if resp.status == 400:
                            print('response:', response, 'input_data:', json.loads(input_data))
                            raise ClientConnectionError
                        return response
                async with session.get(url=url, headers=headers) as resp:
                    response = await resp.json()
                    if resp.status != 200:
                        raise ClientConnectionError
                    return response
            except ClientConnectionError:
                retry_count -= 1
