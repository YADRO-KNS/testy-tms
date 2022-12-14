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
import logging
from datetime import datetime

import redis
from asgiref.sync import async_to_sync
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django.conf import settings
from django.contrib.auth import get_user_model
from testrail_migrator.migrator_lib import TestRailClient, TestrailConfig, TestyCreator
from testrail_migrator.models import TestrailBackup


@shared_task(bind=True)
def upload_task(self, backup_name, user_id):
    user = get_user_model().objects.get(pk=user_id)
    progress_recorder = ProgressRecorder(self)
    max_progress = 7
    progress_recorder.set_progress(0, max_progress, 'Started uploading')
    redis_client = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT)
    backup = json.loads(redis_client.get(backup_name))
    creator = TestyCreator()
    project = creator.create_project(backup['project'])
    progress_recorder.set_progress(1, max_progress, 'Uploading project')
    logging.info('Project finished')
    suites_mappings = creator.create_suites(backup['suites'], project.id)
    progress_recorder.set_progress(2, max_progress, 'Uploading suites')
    logging.info('Suites finished')
    cases_mappings = creator.create_cases(backup['cases'], suites_mappings, project.id)
    progress_recorder.set_progress(3, max_progress, 'Uploading cases')
    logging.info('Cases finished')
    config_mappings = creator.create_configs(backup['configs'], project.id)
    progress_recorder.set_progress(4, max_progress, 'Uploading configs')
    logging.info('Configs finished')
    milestones_mappings = creator.create_milestones(backup['milestones'], project.id)
    progress_recorder.set_progress(5, max_progress, 'Uploading milestones')
    logging.info('milestones_mappings finished')
    plans_mappings = creator.create_plans(backup['plans'], milestones_mappings, project.id)
    progress_recorder.set_progress(6, max_progress, 'Uploading plans')
    logging.info('plans_mappings finished')
    test_mappings = creator.create_runs_parent_plan(
        runs=backup['runs_parent_plan'],
        plan_mappings=plans_mappings,
        config_mappings=config_mappings,
        tests=backup['tests_parent_plan'],
        case_mappings=cases_mappings,
        project_id=project.id
    )
    progress_recorder.set_progress(7, max_progress, 'Uploading tests')
    creator.create_results(backup['results_parent_plan'], test_mappings, user)


@shared_task(bind=True)
def download_task(self, project_id, config_dict, create_dump: bool, dumpfile_path):
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 1, 'Started downloading')
    results = download(project_id, TestrailConfig(**config_dict))
    results_json = json.dumps(results)
    redis_client = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT)
    logging.info(f'REDIS CLIEN PING {redis_client.ping()}')
    backup_name = f'backup{datetime.now()}'
    TestrailBackup.objects.create(name=backup_name, filepath=backup_name)
    redis_client.set(backup_name, results_json)
    if not redis_client.get(backup_name):
        logging.error('REDIS CLIENT GET GOT NOTHING')


@async_to_sync
async def download(project_id: int, config: TestrailConfig):
    async with TestRailClient(config) as testrail_client:
        resulting_data = {'project': await testrail_client.get_project(project_id)}
        # resulting_data.update(await testrail_client.download_descriptions(project_id))
        # resulting_data.update(await testrail_client.download_representations(project_id))
    return resulting_data
