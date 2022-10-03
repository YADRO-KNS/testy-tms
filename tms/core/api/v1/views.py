from rest_framework.viewsets import ModelViewSet

from core.api.v1.serializers import ProjectSerializer
from core.models import Project


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
