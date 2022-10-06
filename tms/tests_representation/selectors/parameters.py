from django.db.models import QuerySet

from tests_representation.models import Parameter


class ParameterSelector:
    def parameter_list(self) -> QuerySet[Parameter]:
        return Parameter.objects.all()
