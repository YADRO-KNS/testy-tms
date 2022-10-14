from django.utils import timezone

USERNAME = 'test_user'
PASSWORD = '123qweasd123'
NEW_PASSWORD = 'qweasd123qwe'
INVALID_PASSWORD = 'qwerty'
USER_EMAIL = 'user@example.com'
INVALID_EMAIL = 'user@example'
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
DATE = timezone.now()
STATUS_NAME = 'PASSED'
STATUS_CODE = 1
TEST_COMMENT = 'TestComment'
GROUP_NAME = 'TestGroup'
PARAMETER_GROUP_NAME = 'OS'
PARAMETER_DATA = 'LINUX'
TEST_PLAN_NAME = 'TestPlan'
EXCEEDING_CHAR_FIELD = 't' * 256

NUMBER_OF_OBJECTS_TO_CREATE = 10
