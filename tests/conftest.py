import pytest
from rest_framework.test import APIClient

from tests.factories import (
    ParameterFactory,
    ProjectFactory,
    TestCaseFactory,
    TestFactory,
    TestPlanFactory,
    TestResultFactory,
    TestSuiteFactory,
    UserFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope='function')
def default_user():
    yield UserFactory.create(username='default_test_user')


@pytest.fixture(scope='function')
def admin_user():
    yield UserFactory.create(username='admin_test_user', is_staff=True)


@pytest.fixture(scope='function')
def authorized_default_user(default_user, api_client):
    yield api_client.force_login(default_user)


@pytest.fixture(scope='function')
def authorized_superuser(admin_user, api_client):
    yield api_client.force_login(admin_user)


@pytest.fixture(scope='function')
def project():
    yield ProjectFactory.create(name='project_fixture')


@pytest.fixture(scope='function')
def test_suite():
    yield TestSuiteFactory.create(name='test_suite_fixture')


@pytest.fixture(scope='function')
def test_case():
    yield TestCaseFactory.create(name='test_case_fixture')


@pytest.fixture(scope='function')
def test_result():
    yield TestResultFactory.create()


@pytest.fixture(scope='function')
def test():
    yield TestFactory.create()


@pytest.fixture(scope='function')
def parameter():
    yield ParameterFactory.create()


@pytest.fixture(scope='function')
def test_plan():
    yield TestPlanFactory.create()
