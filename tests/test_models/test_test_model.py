import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from tests_representation.models import Test

from tests.error_messages import NOT_NULL_ERR_MSG


@pytest.mark.django_db
class TestTestModel:
    relation_name = Test._meta.label_lower.replace('.', '_')

    @pytest.mark.parametrize('parameter_name', ['case', 'plan', 'user', 'is_archive'])
    def test_not_null_constraint(self, parameter_name, test_factory):
        foreign_keys = ['case', 'plan', 'user']
        with pytest.raises(IntegrityError) as err:
            test_factory(**{parameter_name: None})
        parameter_name = f'{parameter_name}_id' if parameter_name in foreign_keys else parameter_name
        assert NOT_NULL_ERR_MSG.format(
            relation=self.relation_name, column=parameter_name
        ) in str(err.value), 'Expected error message was not found.'

    @pytest.mark.parametrize(
        'parameter_name, incorrect_value, error_type', [
            ('case', 'abc', ValueError),
            ('plan', 'abc ', ValueError),
            ('user', 'abc ', ValueError),
            ('is_archive', 'abc', ValidationError)
        ]
    )
    def test_fields_type_constraint(self, parameter_name, incorrect_value, error_type, test_factory):
        with pytest.raises(error_type):
            test_factory(**{parameter_name: incorrect_value})

    def test_valid_model_creation(self, test):
        assert Test.objects.count() == 1
        assert Test.objects.get(id=test.id) == test
