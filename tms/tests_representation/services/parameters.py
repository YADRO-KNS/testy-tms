from typing import Any, Dict

from tests_representation.models import Parameter


class ParameterService:
    non_side_effect_fields = ['project', 'data', 'group_name']

    def parameter_create(self, data: Dict[str, Any]) -> Parameter:
        return Parameter.model_create(
            fields=self.non_side_effect_fields,
            data=data,
            commit=True,
        )

    def parameter_update(self, parameter: Parameter, data: Dict[str, Any]) -> Parameter:
        parameter, has_updated = parameter.model_update(
            fields=self.non_side_effect_fields,
            data=data,
            commit=True,
        )
        return parameter
