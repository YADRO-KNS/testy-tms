import constants
from core.models import Project
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory
from tests_description.models import TestCase, TestSuite
from tests_representation.models import Test, TestPlan, TestResult, TestStatus

UserModel = get_user_model()


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


class TestPlanFactory(DjangoModelFactory):
    class Meta:
        model = TestPlan

    started_at = constants.DATE
    due_date = constants.DATE
    finished_at = constants.DATE
    is_archive = False


class TestResultsFactory(DjangoModelFactory):
    class Meta:
        model = TestResult


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = Sequence(lambda n: f'{constants.PROJECT_NAME}{n}')
    description = constants.DESCRIPTION


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


class TestStatusFactory(DjangoModelFactory):
    class Meta:
        model = TestStatus

    name = constants.STATUS_NAME
    status_code = constants.STATUS_CODE


class TestResultFactory(DjangoModelFactory):
    class Meta:
        model = TestResult

    test = SubFactory(TestFactory)
    status = SubFactory(TestStatus)
