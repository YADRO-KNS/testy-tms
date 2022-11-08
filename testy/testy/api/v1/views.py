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

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import APIRootView


class V1RootView(APIRootView):
    def get_view_name(self):
        return 'v1'

    def get(self, request, format=None):
        return Response({
            'projects': reverse('api:v1:project-list', request=request, format=format),
            'suites': reverse('api:v1:testsuite-list', request=request, format=format),
            'cases': reverse('api:v1:testcase-list', request=request, format=format),
            'tests': reverse('api:v1:test-list', request=request, format=format),
            'results': reverse('api:v1:testresult-list', request=request, format=format),
            'testplans': reverse('api:v1:testplan-list', request=request, format=format),
            'parameters': reverse('api:v1:parameter-list', request=request, format=format),
            'users': reverse('api:v1:user-list', request=request, format=format),
            'groups': reverse('api:v1:group-list', request=request, format=format),
            'attachments': reverse('api:v1:attachment-list', request=request, format=format)
        })
