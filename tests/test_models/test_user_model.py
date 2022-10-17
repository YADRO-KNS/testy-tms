import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from tests.error_messages import ALREADY_EXISTS_ERR_MSG, BOOL_VALUE_ERR_MSG, NOT_NULL_ERR_MSG

UserModel = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    relation_name = UserModel._meta.label_lower.replace('.', '_')

    @pytest.mark.parametrize('parameter_name', ['username', 'password', 'is_active', 'is_staff', 'is_superuser'])
    def test_not_null_constraint(self, parameter_name, user_factory):
        with pytest.raises(IntegrityError) as err:
            user_factory(**{parameter_name: None})
        assert NOT_NULL_ERR_MSG.format(relation=self.relation_name, column=parameter_name) in str(err.value), \
            'Expected error message was not found.'

    @pytest.mark.parametrize(
        'parameter_name, incorrect_value', [
            ('is_superuser', 'abc'),
            ('is_active', 'abc'),
            ('is_staff', 'abc')
        ]
    )
    def test_fields_type_constraint(self, parameter_name, incorrect_value, user_factory):
        with pytest.raises(ValidationError) as err:
            user_factory(**{parameter_name: incorrect_value})
        assert BOOL_VALUE_ERR_MSG.format(value=incorrect_value) in str(err.value)

    def test_duplicate_username_not_allowed(self, user, user_factory):
        with pytest.raises(IntegrityError) as err:
            user_factory(username=user.username)
        assert ALREADY_EXISTS_ERR_MSG.format(
            column_name='username', column_value=user.username
        ) in str(err.value), f'Expected error message was not found. Expected message: {ALREADY_EXISTS_ERR_MSG}'

    def test_valid_model_creation(self, user):
        assert UserModel.objects.count() == 1
        assert UserModel.objects.get(id=user.id) == user
