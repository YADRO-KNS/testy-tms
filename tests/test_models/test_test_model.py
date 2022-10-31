# TMS - Test Management System
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
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from tests_representation.models import Test

from tests.error_messages import BOOL_VALUE_ERR_MSG, MODEL_VALUE_ERR_MSG, NOT_NULL_ERR_MSG


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
        'parameter_name, incorrect_value, error_type, err_msg', [
            ('case', 'abc', ValueError, MODEL_VALUE_ERR_MSG.format(value='abc', model_name='Test', column_name='case',
                                                                   column_model='TestCase')),
            ('plan', 'abc', ValueError, MODEL_VALUE_ERR_MSG.format(value='abc', model_name='Test', column_name='plan',
                                                                   column_model='TestPlan')),
            ('user', 'abc', ValueError, MODEL_VALUE_ERR_MSG.format(value='abc', model_name='Test', column_name='user',
                                                                   column_model='User')),
            ('is_archive', 'abc', ValidationError, BOOL_VALUE_ERR_MSG.format(value='abc'))
        ]
    )
    def test_fields_type_constraint(self, parameter_name, incorrect_value, error_type, test_factory, err_msg):
        with pytest.raises(error_type) as err:
            test_factory(**{parameter_name: incorrect_value})
        assert err_msg in str(err.value)

    def test_valid_model_creation(self, test):
        assert Test.objects.count() == 1
        assert Test.objects.get(id=test.id) == test
