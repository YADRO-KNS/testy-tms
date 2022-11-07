
import pytest
from django.db import IntegrityError
from tests_description.models import TestCase

from tests.error_messages import INT_VALUE_ERR_MSG, MODEL_VALUE_ERR_MSG, NOT_NULL_ERR_MSG


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
        'parameter_name, incorrect_value, err_msg', [
            ('project', 'abc', MODEL_VALUE_ERR_MSG.format(value='abc', model_name='TestCase', column_name='project',
                                                          column_model='Project')),
            ('suite', 'abc', MODEL_VALUE_ERR_MSG.format(value='abc', model_name='TestCase', column_name='suite',
                                                        column_model='TestSuite')),
            ('estimate', 'abc', INT_VALUE_ERR_MSG.format(column='estimate', value='abc')),
        ]
    )
    def test_fields_type_constraint(self, parameter_name, incorrect_value, err_msg, test_case_factory):
        with pytest.raises(ValueError) as err:
            test_case_factory(**{parameter_name: incorrect_value})
        assert err_msg == str(err.value)

    def test_valid_model_creation(self, test_case):
        assert TestCase.objects.count() == 1
        assert TestCase.objects.get(id=test_case.id) == test_case
