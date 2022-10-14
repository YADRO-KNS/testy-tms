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
    data = constants.PARAMETER_DATA
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
    is_archive = False


class TestResultFactory(DjangoModelFactory):
    class Meta:
        model = TestResult

    test = SubFactory(TestFactory)
    status = TestStatuses.UNTESTED
    comment = constants.TEST_COMMENT
