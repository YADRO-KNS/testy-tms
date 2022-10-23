from typing import Optional

from core.models import Project
from django.db.models import QuerySet


class ProjectSelector:

    @staticmethod
    def project_list() -> QuerySet[Project]:
        return QuerySet(model=Project).order_by('name')

    @staticmethod
    def project(project_id) -> Optional[Project]:
        return Project.objects.get(pk=project_id)
