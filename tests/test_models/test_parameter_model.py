import pytest
from django.db import IntegrityError
from tests_representation.models import Parameter

from tests.error_messages import ALREADY_EXISTS_ERR_MSG, NOT_NULL_ERR_MSG


@pytest.mark.django_db
class TestParameterModel:
    relation_name = Parameter._meta.label_lower.replace('.', '_')

    @pytest.mark.parametrize('parameter_name', ['project', 'data', 'group_name'])
    def test_not_null_constraint(self, parameter_name, parameter_factory):
        with pytest.raises(IntegrityError) as err:
            parameter_factory(**{parameter_name: None})
        parameter_name = f'{parameter_name}_id' if parameter_name == 'project' else parameter_name
        assert NOT_NULL_ERR_MSG.format(relation=self.relation_name, column=parameter_name) in str(err.value), \
            'Expected error message was not found.'

    @pytest.mark.parametrize('parameter_name, incorrect_value, error_type', [('project', 1, ValueError)])
    def test_fields_type_constraint(self, parameter_name, incorrect_value, error_type, parameter_factory):
        with pytest.raises(error_type):
            parameter_factory(**{parameter_name: incorrect_value})

    def test_valid_model_creation(self, parameter):
        assert Parameter.objects.count() == 1
        assert Parameter.objects.get(id=parameter.id) == parameter

    def test_unique_together_constraint(self, parameter, parameter_factory):
        with pytest.raises(IntegrityError) as err:
            parameter_factory(group_name=parameter.group_name, data=parameter.data)
        assert ALREADY_EXISTS_ERR_MSG.format(
            column_name='group_name, data',
            column_value=f'{parameter.group_name}, {parameter.data}'
        ) in str(err.value)
