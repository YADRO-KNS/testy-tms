
import pytest
from django.db import IntegrityError
from users.models import Group

from tests.error_messages import NOT_NULL_ERR_MSG


@pytest.mark.django_db
class TestGroupModel:

    @pytest.mark.parametrize('parameter_name', ['name'])
    def test_not_null_constraint(self, parameter_name, group_factory):
        with pytest.raises(IntegrityError) as err:
            group_factory(**{parameter_name: None})
        assert NOT_NULL_ERR_MSG.format(relation='auth_group', column=parameter_name) in str(err.value), \
            'Expected error message was not found.'

    def test_valid_model_creation(self, group):
        assert Group.objects.count() == 1
        assert Group.objects.get(id=group.id) == group
