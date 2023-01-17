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
from core.api.v1.serializers import ProjectSerializer
from core.models import Project
from core.services.projects import ProjectService
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from simple_history.utils import bulk_create_with_history
from tests_description.models import TestCase, TestSuite
from tests_description.services.cases import TestCaseService
from tests_description.services.suites import TestSuiteService
from tests_representation.models import Parameter, Test, TestPlan
from tests_representation.services.parameters import ParameterService
from tests_representation.services.testplans import TestPlanService
from tests_representation.services.tests import TestService
from users.services.users import UserService

UserModel = get_user_model()


class MigratorService:
    @staticmethod
    def suite_create(data) -> TestSuite:
        non_side_effect_fields = TestSuiteService.non_side_effect_fields
        suite = TestSuite.model_create(
            fields=non_side_effect_fields,
            data=data,
        )
        TestSuite.objects.rebuild()
        return suite

    @staticmethod
    def suites_bulk_create(data_list):
        suites = []
        non_side_effect_fields = TestSuiteService.non_side_effect_fields
        for data in data_list:
            test_suite = TestSuite.model_create(non_side_effect_fields, data=data, commit=False)
            test_suite.lft = 0
            test_suite.rght = 0
            test_suite.tree_id = 0
            test_suite.level = 0
            suites.append(test_suite)
        TestSuite.objects.rebuild()
        return TestSuite.objects.bulk_create(suites)

    @staticmethod
    def cases_bulk_create(data_list):
        non_side_effect_fields = TestCaseService.non_side_effect_fields
        cases = []
        for data in data_list:
            cases.append(TestCase.model_create(fields=non_side_effect_fields, data=data, commit=False))

        return bulk_create_with_history(cases, TestCase)

    @staticmethod
    def case_update(case: TestCase, data) -> TestCase:
        non_side_effect_fields = TestCaseService.non_side_effect_fields
        case, _ = case.model_update(
            fields=non_side_effect_fields,
            data=data,
        )
        return case

    @staticmethod
    def parameter_bulk_create(data_list):
        non_side_effect_fields = ParameterService.non_side_effect_fields
        parameters = [Parameter.model_create(fields=non_side_effect_fields, data=data, commit=False) for data in
                      data_list]
        return Parameter.objects.bulk_create(parameters)

    @staticmethod
    def testplan_bulk_create_with_tests(data_list):
        testplan_objects = []
        for data in data_list:
            parameters = data.get('parameters')
            testplan_objects.append(
                TestPlanService()._make_testplan_model(data, parameters=parameters if parameters else None)
            )
        test_plans = TestPlan.objects.bulk_create(testplan_objects)
        TestPlan.objects.rebuild()
        created_tests = []
        for test_plan, data in zip(test_plans, data_list):
            if data.get('test_cases'):
                created_tests.extend(TestService().bulk_test_create([test_plan], data['test_cases']))
        return created_tests, test_plans

    @staticmethod
    def testplan_bulk_create(validated_data):
        testplan_objects = []
        for data in validated_data:
            testplan_objects.append(TestPlanService()._make_testplan_model(data))
        test_plans = TestPlan.objects.bulk_create(testplan_objects)
        TestPlan.objects.rebuild()

        return test_plans

    @staticmethod
    def create_project(project) -> Project:
        data = {
            'name': project['name'],
            'description': project['announcement'] if project['announcement'] else ''
        }
        serializer = ProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return ProjectService().project_create(serializer.validated_data)

    @staticmethod
    def tests_bulk_create_by_data_list(data_list):
        non_side_effect_fields = TestService.non_side_effect_fields
        test_objects = [Test.model_create(fields=non_side_effect_fields, data=data, commit=False) for data in
                        data_list]
        return Test.objects.bulk_create(test_objects)

    @staticmethod
    def user_create(data) -> UserModel:
        non_side_effect_fields = UserService.non_side_effect_fields
        user = UserModel.model_create(
            fields=non_side_effect_fields,
            data=data,
            commit=False,
        )
        try:
            user.save()
        except IntegrityError:
            user = UserModel.objects.get(username=data['username'])

        return user
