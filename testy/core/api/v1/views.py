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

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.api.v1.serializers import ProjectSerializer
from core.selectors.projects import ProjectSelector
from tests_description.api.v1.serializers import TestSuiteTreeSerializer
from tests_description.selectors.suites import TestSuiteSelector
from tests_representation.api.v1.serializers import ParameterSerializer, TestPlanTreeSerializer
from tests_representation.selectors.parameters import ParameterSelector
from tests_representation.selectors.testplan import TestPlanSelector


class ProjectViewSet(ModelViewSet):
    queryset = ProjectSelector.project_list()
    serializer_class = ProjectSerializer

    @action(detail=False)
    def suites_by_project(self, request, pk):
        qs = TestSuiteSelector().suite_project_root_list(pk)
        serializer = TestSuiteTreeSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def testplans_by_project(self, request, pk):
        qs = TestPlanSelector().testplan_project_root_list(project_id=pk)
        serializer = TestPlanTreeSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def parameters_by_project(self, request, pk):
        qs = ParameterSelector().parameter_project_list(project_id=pk)
        serializer = ParameterSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    # @action(detail=False)
    # def suites_by_project(self, request):
    #     project = request.GET.get('project')
    #     treeview = bool(request.GET.get('treeview'))
    #     qs = ProjectSelector().project_by_id(project)
    #     qs = TestSuiteSelector().suite_project_root_list(project)
    #     serializer = TestSuiteTreeSerializer(qs, many=True, context={'request': request})
    #     return Response(serializer.data)
