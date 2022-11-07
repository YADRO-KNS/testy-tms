
from typing import List, Optional

from django.db.models import QuerySet
from tests_representation.models import Parameter


class ParameterSelector:
    def parameter_list(self) -> QuerySet[Parameter]:
        return Parameter.objects.all()

    def parameters_by_project_id(self, project_id: int) -> QuerySet[Parameter]:
        return QuerySet(model=Parameter).filter(project=project_id).order_by('group_name')

    def parameter_project_list(self, project_id: int) -> QuerySet[Parameter]:
        return QuerySet(model=Parameter).filter(project=project_id).order_by('data')

    def parameter_name_list_by_ids(self, ids: List[int]) -> QuerySet[Optional[List[str]]]:
        return QuerySet(model=Parameter).filter(id__in=ids).values_list('data', flat=True).order_by('data')
