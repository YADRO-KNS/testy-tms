from datetime import datetime

import pytz
from core.api.v1.serializers import ProjectSerializer
from core.models import Project
from core.services.attachments import AttachmentService
from core.services.projects import ProjectService
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from simple_history.utils import bulk_create_with_history
from testrail_migrator.migrator_lib.utils import suppress_auto_now
from tests_description.models import TestCase, TestSuite
from tests_description.selectors.cases import TestCaseSelector
from tests_representation.models import Parameter, Test, TestPlan, TestResult
from tests_representation.services.testplans import TestPlanService
from tests_representation.services.tests import TestService

UserModel = get_user_model()


class MigratorService:
    @staticmethod
    def suite_create(data) -> TestSuite:
        non_side_effect_fields = ['parent', 'project', 'name', 'description']
        suite = TestSuite.model_create(
            fields=non_side_effect_fields,
            data=data,
        )
        TestSuite.objects.rebuild()
        return suite

    @staticmethod
    def suites_bulk_create(data_list):
        suites = []
        non_side_effect_fields = ['parent', 'project', 'name']
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
        non_side_effect_fields = ['name', 'project', 'suite', 'setup', 'scenario', 'teardown', 'estimate']
        cases = []
        for data in data_list:
            case = TestCase.model_create(fields=non_side_effect_fields, data=data, commit=False)
            case.updated_at = datetime.fromtimestamp(data['updated_at'], tz=pytz.UTC)
            case.created_at = datetime.fromtimestamp(data['created_at'], tz=pytz.UTC)
            cases.append(case)
        with suppress_auto_now(TestCase, ['created_at', 'updated_at']):
            created_cases = bulk_create_with_history(cases, TestCase)
        return created_cases

    @staticmethod
    def case_update(case: TestCase, data) -> TestCase:
        non_side_effect_fields = ['name', 'project', 'suite', 'setup', 'scenario', 'teardown', 'estimate',
                                  'description']
        case, _ = case.model_update(
            fields=non_side_effect_fields,
            data=data,
        )
        return case

    @staticmethod
    def parameter_bulk_create(data_list):
        non_side_effect_fields = ['project', 'data', 'group_name']
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
    @transaction.atomic
    def result_create(data, user) -> TestResult:
        non_side_effect_fields = [
            'status', 'user', 'test', 'comment', 'is_archive', 'test_case_version', 'execution_time', 'created_at',
            'updated_at'
        ]
        test_result: TestResult = TestResult.model_create(
            fields=non_side_effect_fields,
            data=data,
            commit=False,
        )
        test_result.user = user
        test_result.project = test_result.test.case.project
        test_result.test_case_version = TestCaseSelector().case_version(test_result.test.case)
        test_result.full_clean()
        test_result.save()

        for attachment in data.get('attachments', []):
            AttachmentService().attachment_set_content_object(attachment, test_result)

        return test_result

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
        non_side_effect_fields = ['case', 'plan', 'user', 'is_archive', 'project']
        test_objects = [Test.model_create(fields=non_side_effect_fields, data=data, commit=False) for data in
                        data_list]
        return Test.objects.bulk_create(test_objects)

    @staticmethod
    def user_create(data) -> UserModel:
        non_side_effect_fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']
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
