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
