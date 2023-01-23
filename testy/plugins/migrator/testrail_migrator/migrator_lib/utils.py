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
import json
from contextlib import contextmanager
from datetime import datetime
from typing import Any


def back_up(dict_to_backup, path, name):
    with open(f'{path}/{name}{datetime.now()}.json', 'w') as file:
        file.write(json.dumps(dict_to_backup, indent=2))


@contextmanager
def timer(function_name: str):
    start_time = datetime.now()
    yield
    print(f'{function_name} took: ', datetime.now() - start_time)


def split_list_by_chunks(src_list: list, chunk_size: int = 40):
    return [src_list[x:x + chunk_size] for x in range(0, len(src_list), chunk_size)]


def find_idx_by_key_value(key: str, value: Any, src_list: list):
    for idx, elem in enumerate(src_list):
        if elem[key] == value:
            return idx


@contextmanager
def suppress_auto_now(model, field_names):
    """
    Suppress auto_now and auto_now_add options in model fields.

    Function is not supposed to be used inside Django app, may cause breaking of auto fields. Not supposed to be used
    in views/forms/serializers etc.

    Args:
        model: Model class
        field_names: name of fields with auto content
    """
    fields_state = {}
    for field_name in field_names:
        field = model._meta.get_field(field_name)
        fields_state[field] = {'auto_now': field.auto_now, 'auto_now_add': field.auto_now_add}

    for field in fields_state:
        field.auto_now = False
        field.auto_now_add = False
    try:
        yield
    finally:
        for field, state in fields_state.items():
            field.auto_now = state['auto_now']
            field.auto_now_add = state['auto_now_add']
