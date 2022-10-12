from core.models import Project
from django.db.models import QuerySet


class ProjectSelector:

    @staticmethod
    def project_list() -> QuerySet[Project]:
        return QuerySet(model=Project).order_by('name')
