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

NOT_NULL_ERR_MSG = 'null value in column "{column}" of relation "{relation}" violates not-null constraint'
CHAR_LENGTH_ERR_MSG = 'value too long for type character varying(255)\n'
ALREADY_EXISTS_ERR_MSG = 'Key ({column_name})=({column_value}) already exists.'
INVALID_EMAIL_MSG = 'Enter a valid email address.'
UNAUTHORIZED_MSG = 'Authentication credentials were not provided.'
REQUIRED_FIELD_MSG = 'This field is required.'
BOOL_VALUE_ERR_MSG = '“{value}” value must be either True or False.'
MODEL_VALUE_ERR_MSG = 'Cannot assign "\'{value}\'": "{model_name}.{column_name}" must be a "{column_model}" instance.'
INT_VALUE_ERR_MSG = "Field '{column}' expected a number but got '{value}'."
ARRAY_VALUE_ERR_MSG = 'Array value must start with "{" or dimension information.'
TYPE_ERR_MSG = 'expected string or bytes-like object'
