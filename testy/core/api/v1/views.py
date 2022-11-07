
from core.api.v1.serializers import ProjectSerializer
from core.selectors.projects import ProjectSelector
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
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
