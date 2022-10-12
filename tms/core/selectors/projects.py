from django.db.models import QuerySet

from core.models import Project


class ProjectSelector:

    @staticmethod
    def project_list() -> QuerySet[Project]:
        return QuerySet(model=Project).order_by('name')
