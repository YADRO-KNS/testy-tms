
from core.models import Project
from django.db.models import QuerySet


class ProjectSelector:

    @staticmethod
    def project_list() -> QuerySet[Project]:
        return QuerySet(model=Project).order_by('name')

    @staticmethod
    def project_by_id(project_id: int) -> Project:
        return QuerySet(model=Project).get(pk=project_id)
