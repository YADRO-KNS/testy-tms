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
import logging
import os
import time
from contextlib import contextmanager
from hashlib import md5
from typing import List

from celery_progress.backend import ProgressRecorder


class ProgressRecorderContext(ProgressRecorder):
    def __init__(self, task, total, debug=False, description='Task started'):
        self.debug = debug
        self.current = 0
        self.total = total
        if self.debug:
            return
        super().__init__(task)
        self.set_progress(current=self.current, total=total, description=description)

    @contextmanager
    def progress_context(self, description):
        if self.debug:
            logging.info(description)
            yield
            return
        self.current += 1
        self.set_progress(self.current, self.total, description)
        yield

    def clear_progress(self):
        self.current = 0


def get_attachments_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f'{md5(str(time.time()).encode()).hexdigest()}{extension}'
    return f'attachments/{filename[0:2]}/{filename}'


def parse_bool_from_str(value):
    if str(value).lower() in ['1', 'yes', 'true']:
        return True
    return False


def form_tree_prefetch_query(nested_prefetch_field: str, prefetch_field: str, tree_depth) -> List[str]:
    queries = [prefetch_field]
    for count in range(1, tree_depth + 1):
        query = '__'.join([nested_prefetch_field for _ in range(count)]) + '__' + prefetch_field
        queries.append(query)
    return queries
