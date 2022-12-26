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

from enum import Enum
from http import HTTPStatus
from typing import Any, Dict, List, Union

from django.db.models import QuerySet
from django.forms import model_to_dict
from django.test.client import RequestFactory
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class RequestType(Enum):
    POST = 'post'
    GET = 'get'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'


class RequestMock(RequestFactory):
    GET = {}

    @staticmethod
    def build_absolute_uri(url):
        return f'http://testserver{url}'


class CustomAPIClient(APIClient):
    def send_request(
            self,
            view_name: str,
            data: Dict[str, Any] = None,
            expected_status: HTTPStatus = HTTPStatus.OK,
            request_type: RequestType = RequestType.GET,
            reverse_kwargs: Dict[str, Any] = None,
            format='json',
            query_params: Dict[str, Any] = None
    ):
        url = reverse(view_name, kwargs=reverse_kwargs)
        if query_params:
            url = f'{url}?{"&".join([f"{field}={field_value}" for field, field_value in query_params.items()])}'
        http_request = getattr(self, request_type.value, None)
        if not http_request:
            raise TypeError('Request type is not known')
        response = http_request(url, data=data, format=format)

        assert response.status_code == expected_status, f'Expected response code "{expected_status}", ' \
                                                        f'actual: "{response.status_code}"' \
                                                        f'Response content: {response.content}'
        return response


def model_with_base_to_dict(instance) -> Dict[str, Any]:
    instance_dict = model_to_dict(instance)
    instance_dict['created_at'] = instance.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    instance_dict['updated_at'] = instance.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return instance_dict


def model_to_dict_via_serializer(instances: Union[QuerySet, Any], serializer_class, many=False) -> List[dict]:
    serializer = serializer_class(instances if many else instances[0], many=many, context={'request': RequestMock()})
    return [dict(elem) for elem in serializer.data] if many else dict(serializer.data)
