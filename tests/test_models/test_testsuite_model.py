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
from django.db import IntegrityError
from tests_description.models import TestSuite

from tests.error_messages import MODEL_VALUE_ERR_MSG, NOT_NULL_ERR_MSG

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
