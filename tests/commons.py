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
        if request_type == RequestType.GET:
            response = self.get(url)
        elif request_type == RequestType.POST:
            response = self.post(url, data=data)
        elif request_type == RequestType.PATCH:
            response = self.patch(url, data=data)
        elif request_type == RequestType.PUT:
            response = self.put(url, data=data)
        elif request_type == RequestType.DELETE:
            response = self.delete(url)
        else:
            raise TypeError('Request type is not known')

        assert response.status_code == expected_status, f'Expected response code "{expected_status}", ' \
                                                        f'actual: "{response.status_code}"'
        return response


def model_with_base_to_dict(instance) -> Dict[str, Any]:
    instance_dict = model_to_dict(instance)
    instance_dict['created_at'] = instance.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    instance_dict['updated_at'] = instance.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return instance_dict
