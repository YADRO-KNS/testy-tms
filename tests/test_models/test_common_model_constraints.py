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
from django.db import DataError
from tests_description.models import TestCase, TestSuite
from tests_representation.models import Parameter, Test, TestPlan, TestResult

from tests import constants
from tests.error_messages import CHAR_LENGTH_ERR_MSG
from tests.factories import (
    ParameterFactory,
    ProjectFactory,
    TestCaseFactory,
    TestFactory,
    TestPlanFactory,
    TestResultFactory,
    TestSuiteFactory,
)


@pytest.mark.django_db
class TestCommonConstraints:
    @pytest.mark.parametrize(
        'instance, column_name', [
            (TestPlanFactory, 'name'),
            (TestSuiteFactory, 'name'),
            (TestCaseFactory, 'name'),
            (TestPlanFactory, 'name'),
            (ProjectFactory, 'name'),
            (ParameterFactory, 'group_name')
        ]
    )
    def test_char_length_constraint(self, instance, column_name):
        with pytest.raises(DataError) as err:
            instance.create(**{column_name: constants.EXCEEDING_CHAR_FIELD})
        assert CHAR_LENGTH_ERR_MSG == str(err.value), f'Char field length was exceeded in model "{instance}".'

    @pytest.mark.parametrize(
        'child_factory, parent_factory, model, parameter_name', [
            (TestSuiteFactory, TestSuiteFactory, TestSuite, 'parent'),
            (TestSuiteFactory, ProjectFactory, TestSuite, 'project'),
            (TestPlanFactory, TestPlanFactory, TestPlan, 'parent'),
            (TestFactory, TestCaseFactory, Test, 'case'),
            (TestFactory, TestPlanFactory, Test, 'plan'),
            (TestResultFactory, TestFactory, TestResult, 'test'),
            (ParameterFactory, ProjectFactory, Parameter, 'project'),
            (TestCaseFactory, ProjectFactory, TestCase, 'project'),
            (TestCaseFactory, TestSuiteFactory, TestCase, 'suite')
        ]
    )
    def test_cascade_delete(self, parent_factory, child_factory, model, parameter_name):
        expected_number_of_objects = 5
        parent_object = parent_factory.create()

        for _ in range(expected_number_of_objects):
            child_factory.create(**{parameter_name: parent_object})

        objects_number = model.objects.count()
        if parent_factory == child_factory:
            expected_number_of_objects += 1
        assert objects_number == expected_number_of_objects, f'Expected number of {model} is ' \
                                                             f'"{expected_number_of_objects}"' \
                                                             f'actual number of {model} is "{objects_number}"'
        parent_object.delete()
        assert not model.objects.count(), 'Parameters were not deleted with project.'
