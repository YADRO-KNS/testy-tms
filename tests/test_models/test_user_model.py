# TestY TMS - Test Management System
# Copyright (C) 2022 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.

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
