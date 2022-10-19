from itertools import product
from typing import List, Dict, Tuple

from tests_representation.models import Parameter


def combination_parameters(parameters: List[Parameter]) -> List[Tuple[int, ...]]:
    """
    Returns all possible combinations of parameters by group name
    """
    group_parameters = {}

    for parameter in parameters:
        group_parameters.setdefault(parameter.group_name, []).append(parameter.id)

    return list(product(*group_parameters.values()))
