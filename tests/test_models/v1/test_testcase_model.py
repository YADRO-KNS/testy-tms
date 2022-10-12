import pytest
from django.db import IntegrityError
from tests_description.models import TestCase

from tests.error_messages import NOT_NULL_ERR_MSG


@pytest.mark.django_db
class TestCaseModel:
    relation_name = TestCase._meta.label_lower.replace('.', '_')

    @pytest.mark.parametrize('parameter_name', ['name', 'project', 'suite', 'setup', 'scenario', 'teardown'])
    def test_not_null_constraint(self, parameter_name, test_case_factory):
        foreign_keys = ['project', 'suite']
        with pytest.raises(IntegrityError) as err:
            test_case_factory(**{parameter_name: None})
        parameter_name = f'{parameter_name}_id' if parameter_name in foreign_keys else parameter_name
        assert NOT_NULL_ERR_MSG.format(relation=self.relation_name, column=parameter_name) in str(err.value), \
            'Expected error message was not found.'

    @pytest.mark.parametrize(
        'parameter_name, incorrect_value, error_type', [
            ('project', 1, ValueError),
            ('suite', 1, ValueError),
            ('estimate', 'abc', ValueError),
        ]
    )
    def test_fields_type_constraint(self, parameter_name, incorrect_value, error_type, test_case_factory):
        with pytest.raises(error_type):
            test_case_factory(**{parameter_name: incorrect_value})

    def test_valid_model_creation(self, test_case):
        assert TestCase.objects.count() == 1
        assert TestCase.objects.get(id=test_case.id) == test_case
