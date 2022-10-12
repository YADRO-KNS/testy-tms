import pytest
from django.core.exceptions import ValidationError
from django.db import DataError, IntegrityError
from tests_representation.models import TestPlan

from tests.error_messages import NOT_NULL_ERR_MSG


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
        'parameter_name, incorrect_value, error_type', [
            ('parent', 1, ValueError),
            ('parameters', 'abc', DataError),
            ('started_at', 1, TypeError),
            ('due_date', 1, TypeError),
            ('finished_at', 1, TypeError),
            ('is_archive', 'abc', ValidationError)
        ]
    )
    def test_fields_type_constraint(self, parameter_name, incorrect_value, error_type, test_plan_factory):
        with pytest.raises(error_type):
            test_plan_factory(**{parameter_name: incorrect_value})

    def test_valid_model_creation(self, test_plan):
        assert TestPlan.objects.count() == 1
        assert TestPlan.objects.get(id=test_plan.id) == test_plan
