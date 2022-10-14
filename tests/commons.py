from enum import Enum
from http import HTTPStatus
from typing import Any, Dict

from django.forms import model_to_dict
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class RequestType(Enum):
    POST = 'post'
    GET = 'get'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'


class CustomAPIClient(APIClient):
    def send_request(
            self,
            view_name: str,
            data: Dict[str, Any] = None,
            expected_status: HTTPStatus = HTTPStatus.OK,
            request_type: RequestType = RequestType.GET,
            reverse_kwargs: Dict[str, Any] = None

    ):
        url = reverse(view_name, kwargs=reverse_kwargs)
        http_request = getattr(self, request_type.value, None)
        if not http_request:
            raise TypeError('Request type is not known')
        response = http_request(url, data=data)

        assert response.status_code == expected_status, f'Expected response code "{expected_status}", ' \
                                                        f'actual: "{response.status_code}"'
        return response


def model_with_base_to_dict(instance) -> Dict[str, Any]:
    instance_dict = model_to_dict(instance)
    instance_dict['created_at'] = instance.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    instance_dict['updated_at'] = instance.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return instance_dict
