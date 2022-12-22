# TestY TMS - Test Management System
# Copyright (C) 2022 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.
import asyncio
import itertools
import logging
from enum import Enum
from http import HTTPStatus
from json import JSONDecodeError

import aiohttp
import requests
from aiohttp import ClientConnectionError, ContentTypeError
from tqdm.asyncio import tqdm

from .config import TestrailConfig
from .utils import split_list_by_chunks, timer


class InstanceType(Enum):
    PLAN = 'plan'
    CASE = 'case'
    TEST = 'test'
    RUN = 'run'
    ENTRY = 'entry'


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


class TestrailClientSync:
    def __init__(self, config: TestrailConfig):
        """
        Init method for TestRailClient.

        Args:
            config: instance of TestrailConfig
        """
        if not config.login or not config.password:
            raise TestRailClientError('No login or password were provided.')
        self.config = config

    def get_single_attachment(self, attachment_id):
        return self._process_request(endpoint=f'/get_attachment/{attachment_id}')

    def _process_request(self, endpoint: str, retry_count=30):
        """
        Process request to TestRail REST API.

        Args:
            endpoint: endpoint url
            input_data: content

        Returns:
            data or None for error
        """
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        url = self.config.api_url + endpoint
        while retry_count:
            response = requests.get(url, auth=(self.config.login, self.config.password), headers=headers)
            if response.status_code == HTTPStatus.OK:
                return response.content
            logging.error(f'Response not ok - {response}')
            retry_count -= 1


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
        # TODO: add check if auth failed
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

            descriptions_dict['sections'] = await self.get_sections(project_id, descriptions_dict['suites'])

        return descriptions_dict

    async def get_users(self, project_id=''):
        return await self._process_request(f'/get_users/{project_id}')

    async def download_representations(self, project_id: int, ignore_completed: bool):
        representations_dict = {}
        query_params = {'is_completed': 0 if ignore_completed else 1}
        configs = await self.get_configs(project_id)
        representations_dict['configs'] = configs
        milestones = await self.get_milestones(project_id, query_params=query_params)
        for milestone in milestones:
            filtered_children = []
            for child_milestone in milestone['milestones']:
                if ignore_completed and child_milestone['is_completed']:
                    continue
                filtered_children.append(child_milestone)
            milestone['milestones'] = filtered_children

        representations_dict['milestones'] = milestones

        plans_list = await self.get_plans(project_id, query_params=query_params)
        representations_dict['plans'] = await self.get_plans_with_runs(plans_list)

        runs_parent_plan = []
        for plan in representations_dict['plans']:
            for entry in plan['entries']:
                runs_parent_plan.extend(entry['runs'])
        representations_dict['runs_parent_plan'] = runs_parent_plan

        representations_dict['runs_parent_mile'] = await self.get_runs(project_id, query_params=query_params)

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

    async def get_sections_for_suite(self, project_id, suite_id):
        return await self._process_request(f'/get_sections/{project_id}', query_params={'suite_id': suite_id})

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

    async def get_sections(self, project_id, suites):
        sections = []
        suite_chunks = split_list_by_chunks(suites)
        for chunk in tqdm(suite_chunks, desc='Getting sections for suites'):
            tasks = []
            for suite in chunk:
                tasks.append(self.get_sections_for_suite(project_id, suite['id']))
            sections.extend(
                list(itertools.chain.from_iterable(
                    await tqdm.gather(*tasks, desc='Section chunk progress', leave=False))
                )
            )
        return sections

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

    async def get_attachment_with_parent_id(self, instance_id, instance_type: InstanceType):
        attachments = await self._process_request(f'/get_attachments_for_{instance_type.value}/{instance_id}')
        if attachments:
            for attachment in attachments:
                attachment[f'{instance_type.value}_id'] = instance_id
        return attachments if attachments else []

    async def get_attachment_with_parent_id_for_entry(self, plan_id, entry_id):
        attachments = await self._process_request(f'/get_attachments_for_plan_entry/{plan_id}/{entry_id}')
        if attachments:
            for attachment in attachments:
                attachment['plan_id'] = plan_id
        return attachments if attachments else []

    async def get_attachments_for_instances(self, instances: list, instance_type: InstanceType):
        attachments = []
        chunks = split_list_by_chunks(instances)

        for idx, chunk in enumerate(tqdm(chunks, desc=f'{instance_type.value} attachments progress')):
            tasks = []
            if instance_type == InstanceType.ENTRY:
                for instance in chunk:
                    tasks.append(
                        self.get_attachment_with_parent_id_for_entry(instance['plan_id'], instance['id'])
                    )
            # elif instance_type == InstanceType.TEST:
            #     for instance in chunk:
            #         tasks.append(
            #             self.get_attachment_with_parent_id(instance['test_id'], instance_type)
            #         )
            else:
                for instance in chunk:
                    tasks.append(
                        self.get_attachment_with_parent_id(instance['id'], instance_type)
                    )

            attachments.extend(
                list(
                    itertools.chain.from_iterable(
                        await tqdm.gather(*tasks, desc='attachments chunk progress', leave=False)
                    )
                )
            )
        return attachments

    async def get_attachments_from_list(self, attachment_list, parent_key):
        attachments = []
        result = {}
        attachment_chunks = split_list_by_chunks(attachment_list)
        for chunk in tqdm(attachment_chunks):
            tasks = []
            for attachment in chunk:
                tasks.append(self.get_attachment(attachment, parent_key))
            attachments.extend(await tqdm.gather(*tasks, leave=False))
        for attachment in attachments:
            result.update(attachment)
        return result

    async def get_attachment(self, attachment, parent_key, retry_count=30):
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        while retry_count:
            try:
                async with self.session.get(url=self.config.api_url + f'/get_attachment/{attachment["id"]}',
                                            headers=headers) as resp:
                    if resp.status == 400:
                        return
                    if resp.status != 200:
                        raise ClientConnectionError
                    return {
                        attachment['id']: {
                            parent_key: attachment[parent_key],
                            'content_type': resp.content_type,
                            'size': attachment['size'],
                            'charset': resp.charset,
                            'name': attachment['name'],
                            'field_name': 'file',
                            'file_bytes': await resp.read(),
                            'user_id': attachment['user_id'],
                        }
                    }
            except (ClientConnectionError, asyncio.TimeoutError):
                retry_count -= 1

    async def get_single_attachment(self, attachment_id, retry_count=30):
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        while retry_count:
            try:
                async with self.session.get(url=self.config.api_url + f'/get_attachment/{attachment_id}',
                                            headers=headers) as resp:
                    if resp.status != 200:
                        logging.error(resp)
                        raise ClientConnectionError
                    return await resp.read()
            except (ClientConnectionError, asyncio.TimeoutError):
                retry_count -= 1

    # def get_single_attachment(self, attachment_id):
    #     headers = {
    #         'Content-Type': 'application/json; charset=utf-8'
    #     }
    #     url = self.config.api_url + endpoint
    #     logger.debug(f'Request GET - {endpoint}')
    #     response = requests.get(url, auth=(self.config.login, self.config.password), headers=headers)
    #     return response

    async def get_attachments_for_plan(self, plan_id: int):
        list_of_attachments = await self._process_request(f'/get_attachments_for_plan/{plan_id}')
        if list_of_attachments:
            for attachment in list_of_attachments:
                attachment['plan_id'] = plan_id
            return list_of_attachments

    async def get_attachments_for_run(self, run_id: int):
        list_of_attachments = await self._process_request(f'/get_attachments_for_run/{run_id}')
        if list_of_attachments:
            for attachment in list_of_attachments:
                attachment['run_id'] = run_id
            return list_of_attachments

    async def get_attachments_for_test(self, test_id: int):
        list_of_attachments = await self._process_request(f'/get_attachments_for_test/{test_id}')
        if list_of_attachments:
            for attachment in list_of_attachments:
                attachment['test_id'] = test_id
            return list_of_attachments

    async def _process_request(
            self, endpoint: str,
            headers=None,
            query_params=None,
            retry_count: int = 30,
            file: bool = False
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
                    if resp.status == 400:
                        return
                    if resp.status != 200:
                        try:
                            logging.error(await resp.json())
                        except (JSONDecodeError, ContentTypeError):
                            logging.error(await resp.text())
                        raise ClientConnectionError
                    return await resp.read() if file else await resp.json()
            except (ClientConnectionError, asyncio.TimeoutError):
                retry_count -= 1
