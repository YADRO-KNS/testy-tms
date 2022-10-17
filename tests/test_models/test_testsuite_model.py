import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from tests_description.models import TestSuite

from tests.error_messages import NOT_NULL_ERR_MSG, MODEL_VALUE_ERR_MSG

UserModel = get_user_model()


@pytest.mark.django_db
class TestSuiteModel:
    relation_name = TestSuite._meta.label_lower.replace('.', '_')

    @pytest.mark.parametrize('parameter_name', ['project', 'name'])
    def test_not_null_constraint(self, parameter_name, test_suite_factory):
        with pytest.raises(IntegrityError) as err:
            test_suite_factory(**{parameter_name: None})
        parameter_name = f'{parameter_name}_id' if parameter_name == 'project' else parameter_name
        assert NOT_NULL_ERR_MSG.format(relation=self.relation_name, column=parameter_name) in str(err.value), \
            'Expected error message was not found.'

    @pytest.mark.parametrize(
        'parameter_name, incorrect_value, err_msg', [
            ('parent', 'abc', MODEL_VALUE_ERR_MSG.format(value='abc', model_name='TestSuite', column_name='parent',
                                                         column_model='TestSuite')),
            ('project', 'abc', MODEL_VALUE_ERR_MSG.format(value='abc', model_name='TestSuite', column_name='project',
                                                          column_model='Project')),
        ]
    )
    def test_fields_type_constraint(self, parameter_name, incorrect_value, err_msg, test_suite_factory):
        with pytest.raises(ValueError) as err:
            test_suite_factory(**{parameter_name: incorrect_value})
        assert err_msg in str(err.value)

    def test_valid_model_creation(self, test_suite):
        assert TestSuite.objects.count() == 1
        assert TestSuite.objects.get(id=test_suite.id) == test_suite
