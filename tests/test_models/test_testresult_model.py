import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from tests_representation.models import TestResult

from tests.error_messages import BOOL_VALUE_ERR_MSG, INT_VALUE_ERR_MSG, MODEL_VALUE_ERR_MSG, NOT_NULL_ERR_MSG


@pytest.mark.django_db
class TestResultModel:
    relation_name = TestResult._meta.label_lower.replace('.', '_')

    @pytest.mark.parametrize('parameter_name', ['status', 'test', 'is_archive'])
    def test_not_null_constraint(self, parameter_name, test_result_factory):
        with pytest.raises(IntegrityError) as err:
            test_result_factory(**{parameter_name: None})
        parameter_name = 'test_id' if parameter_name == 'test' else parameter_name
        assert NOT_NULL_ERR_MSG.format(relation=self.relation_name, column=parameter_name) in str(err.value), \
            'Expected error message was not found.'

    @pytest.mark.parametrize(
        'parameter_name, incorrect_value, error_type, err_msg', [
            ('status', 'abc', ValueError, INT_VALUE_ERR_MSG.format(column='status', value='abc')),
            ('test', 'abc', ValueError, MODEL_VALUE_ERR_MSG.format(value='abc', model_name='TestResult',
                                                                   column_name='test', column_model='Test')),
            ('user', 'abc', ValueError, MODEL_VALUE_ERR_MSG.format(value='abc', model_name='TestResult',
                                                                   column_name='user', column_model='User')),
            ('is_archive', 'abc', ValidationError, BOOL_VALUE_ERR_MSG.format(value='abc'))
        ]
    )
    def test_fields_type_constraint(self, parameter_name, incorrect_value, error_type, err_msg, test_result_factory):
        with pytest.raises(error_type) as err:
            test_result_factory(**{parameter_name: incorrect_value})
        assert err_msg in str(err.value)

    def test_valid_model_creation(self, test_result):
        assert TestResult.objects.count() == 1
        assert TestResult.objects.get(id=test_result.id) == test_result
