from core.api.v1.serializers import ProjectSerializer
from core.selectors.projects import ProjectSelector
from core.services.projects import ProjectService
from rest_framework.viewsets import ModelViewSet


class ProjectViewSet(ModelViewSet):
    queryset = ProjectSelector.project_list()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer: ProjectSerializer):
        serializer.instance = ProjectService().project_create(serializer.validated_data)

    def perform_update(self, serializer: ProjectSerializer):
        serializer.instance = ProjectService().project_update(serializer.instance, serializer.validated_data)
