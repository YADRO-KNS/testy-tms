import pytest
from django.core.exceptions import ValidationError
from django.db import DataError, IntegrityError
from tests_representation.models import TestPlan

from tests.error_messages import (
    ARRAY_VALUE_ERR_MSG,
    BOOL_VALUE_ERR_MSG,
    MODEL_VALUE_ERR_MSG,
    NOT_NULL_ERR_MSG,
    TYPE_ERR_MSG,
)


@pytest.mark.django_db
class TestPlanModel:
    relation_name = TestPlan._meta.label_lower.replace('.', '_')

    @pytest.mark.parametrize('parameter_name', ['started_at', 'name', 'due_date', 'is_archive'])
    def test_not_null_constraint(self, parameter_name, test_plan_factory):
        with pytest.raises(IntegrityError) as err:
            test_plan_factory(**{parameter_name: None})
        assert NOT_NULL_ERR_MSG.format(relation=self.relation_name, column=parameter_name) in str(err.value), \
            'Expected error message was not found.'

    @pytest.mark.parametrize(
        'parameter_name, incorrect_value, error_type, err_msg', [
            ('parent', 'abc', ValueError, MODEL_VALUE_ERR_MSG.format(value='abc', model_name='TestPlan',
                                                                     column_name='parent', column_model='TestPlan')),
            ('parameters', 'abc', DataError, ARRAY_VALUE_ERR_MSG),
            ('started_at', 1, TypeError, TYPE_ERR_MSG),
            ('due_date', 1, TypeError, TYPE_ERR_MSG),
            ('finished_at', 1, TypeError, TYPE_ERR_MSG),
            ('is_archive', 'abc', ValidationError, BOOL_VALUE_ERR_MSG.format(value='abc'))
        ]
    )
    def test_fields_type_constraint(self, parameter_name, incorrect_value, error_type, err_msg, test_plan_factory):
        with pytest.raises(error_type) as err:
            test_plan_factory(**{parameter_name: incorrect_value})
        assert err_msg in str(err.value)

    def test_valid_model_creation(self, test_plan):
        assert TestPlan.objects.count() == 1
        assert TestPlan.objects.get(id=test_plan.id) == test_plan
