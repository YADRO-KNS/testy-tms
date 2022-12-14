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
from datetime import datetime

import redis
from asgiref.sync import async_to_sync
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django.conf import settings
from testrail_migrator.migrator_lib import TestRailClient, TestrailConfig
from testrail_migrator.models import TestrailBackup


@shared_task(bind=True)
def download_task(self, project_id, config_dict, create_dump: bool, dumpfile_path):
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 1, 'Started downloading')
    results = download(project_id, TestrailConfig(**config_dict))

    r = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT)
    p_mydict = json.dumps(results)
    backup_name = f'backup{datetime.now()}'
    TestrailBackup.objects.create(name=backup_name, filepath=backup_name)
    r.set(backup_name, p_mydict)


@async_to_sync
async def download(project_id: int, config: TestrailConfig):
    async with TestRailClient(config) as testrail_client:
        resulting_data = {'project': await testrail_client.get_project(project_id)}
        resulting_data.update(await testrail_client.download_descriptions(project_id))
        resulting_data.update(await testrail_client.download_representations(project_id))
    return resulting_data
