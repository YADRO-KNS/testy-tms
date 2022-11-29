import json
from copy import deepcopy
from http import HTTPStatus
from typing import Union

import requests

from testrail_migration.config import TestrailConfig


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
        self._auth = (config.login, config.password)
        if not config.login or not config.password:
            raise TestRailClientError('No login or password were provided.')
        self.config = config

    def get_projects(self):
        return self._process_request('/get_projects/')

    def get_suites(self, project_id):
        return self._process_request(f'/get_suites/{project_id}')

    def get_all_suites_for_project(self):
        result = []
        for project in self.get_projects():
            project['suites'] = self.get_suites(project['id'])
            result.append(deepcopy(project))
        return result

    def _process_request(self, endpoint: str, input_data=None) -> Union[list, dict, None]:
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
        if input_data:
            # logger.debug(f'Request POST - {endpoint}, data: {input_data}')
            response = requests.post(url, json=input_data, auth=self._auth, headers=headers)
        else:
            # logger.debug(f'Request GET - {endpoint}')
            response = requests.get(url, auth=self._auth, headers=headers)
        received = json.loads(response.content)
        if response.status_code == HTTPStatus.OK:
            # logger.debug(f'Response ok - {received}')
            return received
        else:
            # logger.warning(f'Response error - status code {response.status_code}, {response.content.decode()}')
            pass
