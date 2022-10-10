import datetime

from rest_framework.reverse import reverse

PROJECTS_URL = reverse('api:v1:project-list')
SUITES_URL = reverse('api:v1:testsuite-list')
SINGLE_SUITE_URL = reverse('api:v1:testsuite-list') + "{id}/"
CASES_URL = reverse('api:v1:testcase-list')
SINGLE_CASE_URL = reverse('api:v1:testcase-list') + "{id}/"
TESTS_URL = reverse('api:v1:test-list')
SINGLE_TEST_URL = reverse('api:v1:test-list') + "{id}/"
RESULTS_URL = reverse('api:v1:testresult-list')
SINGLE_RESULT_URL = reverse('api:v1:testresult-list') + "{id}/"
PARAMETERS_URL = reverse('api:v1:parameter-list')
SINGLE_PARAMETER_URL = reverse('api:v1:parameter-list') + "{id}/"
USERS_URL = reverse('api:v1:user-list')
SINGLE_USER_URL = reverse('api:v1:user-list') + "{id}/"

USERNAME = 'test_user'
PASSWORD = '123qweasd123'
NEW_PASSWORD = 'qweasd123qwe'
NEW_INCORRECT_PASSWORD = 'qwerty'
USER_EMAIL = 'user@example.com'
FIRST_NAME = 'TestFirstName'
LAST_NAME = 'TestLastName'
TEST_SUITE_NAME = 'TestSuiteName'
TEST_CASE_NAME = 'TestCaseName'
PROJECT_NAME = 'TestProjectName'
DESCRIPTION = 'TestDescription'
SETUP = '1.Setup\n2.Setup'
SCENARIO = '1.break\n2.break\n3.break'
TEARDOWN = '1.Teardown\n2.Teardown'
ESTIMATE = 12345
DATE = datetime.datetime.now()
STATUS_NAME = 'PASSED'
STATUS_CODE = 1
TEST_COMMENT = 'TestComment'
GROUP_NAME = 'TestGroup'
PARAMETER_GROUP_NAME = 'OS'
PARAMETER_DATA = 'LINUX'
TEST_PLAN_NAME = 'TestPlan'
