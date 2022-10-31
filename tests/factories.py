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

from core.models import Project
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory
from tests_description.models import TestCase, TestSuite
from tests_representation.choices import TestStatuses
from tests_representation.models import Parameter, Test, TestPlan, TestResult
from users.models import Group

import tests.constants as constants

UserModel = get_user_model()


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = Sequence(lambda n: f'{constants.PROJECT_NAME}{n}')
    description = constants.DESCRIPTION


class ParameterFactory(DjangoModelFactory):
    class Meta:
        model = Parameter

    project = SubFactory(ProjectFactory)
    data = Sequence(lambda n: f'{constants.PARAMETER_DATA}{n}')
    group_name = Sequence(lambda n: f'{constants.PARAMETER_GROUP_NAME}{n}')


class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel

    username = Sequence(lambda n: f'{constants.USERNAME}{n}@yadro.com')
    first_name = constants.FIRST_NAME
    last_name = constants.LAST_NAME
    password = make_password(constants.PASSWORD)
    email = username
    is_active = True
    is_staff = False


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = Sequence(lambda n: f'{constants.GROUP_NAME}{n}')


class TestPlanFactory(DjangoModelFactory):
    class Meta:
        model = TestPlan

    name = Sequence(lambda n: f'{constants.TEST_PLAN_NAME}{n}')
    started_at = constants.DATE
    due_date = constants.DATE
    finished_at = constants.DATE
    project = SubFactory(ProjectFactory)
    is_archive = False


class TestResultsFactory(DjangoModelFactory):
    class Meta:
        model = TestResult


class TestSuiteFactory(DjangoModelFactory):
    class Meta:
        model = TestSuite

    name = Sequence(lambda n: f'{constants.TEST_SUITE_NAME}{n}')
    project = SubFactory(ProjectFactory)


class TestCaseFactory(DjangoModelFactory):
    class Meta:
        model = TestCase

    name = Sequence(lambda n: f'{constants.TEST_CASE_NAME}{n}')
    project = SubFactory(ProjectFactory)
    suite = SubFactory(TestSuiteFactory)
    setup = constants.SETUP
    scenario = constants.SCENARIO
    teardown = constants.TEARDOWN
    estimate = constants.ESTIMATE


class TestFactory(DjangoModelFactory):
    class Meta:
        model = Test

    case = SubFactory(TestCaseFactory)
    plan = SubFactory(TestPlanFactory)
    user = SubFactory(UserFactory)
    project = SubFactory(ProjectFactory)
    is_archive = False


class TestResultFactory(DjangoModelFactory):
    class Meta:
        model = TestResult

    test = SubFactory(TestFactory)
    status = TestStatuses.UNTESTED
    comment = constants.TEST_COMMENT
    project = SubFactory(ProjectFactory)
