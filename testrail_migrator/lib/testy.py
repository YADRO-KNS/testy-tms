import json
from typing import Union

import requests
import urllib3
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

    def create_case(self, case):
        return self._process_request('/cases/', input_data=case)

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
            response = self.session.get(url, headers=headers)
        received = json.loads(response.content)
        # logger.debug(f'Response ok - {received}')
        return received
