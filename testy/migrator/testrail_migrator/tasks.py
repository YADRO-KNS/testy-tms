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
from testrail_migrator.migrator_lib.testrail import InstanceType
from testrail_migrator.models import TestrailBackup


# TODO: переделать чтобы соблюдался принцип DRY
@shared_task(bind=True)
def upload_task(self, backup_name, user_id, config_dict, upload_root_runs: bool = True):
    user = get_user_model().objects.get(pk=user_id)
    progress_recorder = ProgressRecorder(self)

    curr_progress = 0
    max_progress = 7

    progress_recorder.set_progress(curr_progress, max_progress, 'Started uploading')

    redis_client = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT)
    backup = json.loads(redis_client.get(backup_name))
    creator = TestyCreator()

    mappings = {}

    project = creator.create_project(backup['project'])

    keys_without_mappings = ['suites', 'configs', 'milestones']
    for key in keys_without_mappings:
        curr_progress += 1
        create_method = getattr(creator, f'create_{key}')
        progress_recorder.set_progress(curr_progress, max_progress, f'Uploading {key}')
        mappings[key] = create_method(backup[key], project.id)

    keys_with_single_mapping = [('cases', 'suites'), ('plans', 'milestones')]
    for key, mapping_key in keys_with_single_mapping:
        curr_progress += 1
        create_method = getattr(creator, f'create_{key}')
        progress_recorder.set_progress(curr_progress, max_progress, f'Uploading {key}')
        mappings[key] = create_method(backup[key], mappings[mapping_key], project.id)

    mappings['tests_parent_plan'], mappings['runs_parent_plan'] = creator.create_runs_parent_plan(
        runs=backup['runs_parent_plan'],
        plan_mappings=mappings['plans'],
        config_mappings=mappings['configs'],
        tests=backup['tests_parent_plan'],
        case_mappings=mappings['cases'],
        project_id=project.id
    )
    curr_progress += 1
    progress_recorder.set_progress(curr_progress, max_progress, 'Uploading tests')
    mappings['results_parent_plan'] = creator.create_results(backup['results_parent_plan'],
                                                             mappings['tests_parent_plan'], user)

    if upload_root_runs:
        mappings['tests_parent_mile'], mappings['runs_parent_mile'] = creator.create_runs_parent_mile(
            runs=backup['runs_parent_mile'],
            milestone_mappings=mappings['milestones'],
            config_mappings=mappings['configs'],
            tests=backup['tests_parent_mile'],
            case_mappings=mappings['cases'],
            project_id=project.id
        )
        mappings['results_parent_mile'] = creator.create_results(backup['results_parent_mile'],
                                                                 mappings['tests_parent_mile'], user)

    upload_attachments(config_dict, project, user, backup['attachments'], mappings, upload_root_runs)


@async_to_sync
async def upload_attachments(config_dict, project, user, attachments, mappings, upload_root_runs: bool):
    async with TestRailClient(TestrailConfig(**config_dict)) as testrail_client:
        keys = [
            ('cases', 'case_id', InstanceType.CASE),
            ('plans', 'plan_id', InstanceType.PLAN),
            ('runs_parent_plan', 'run_id', InstanceType.RUN),
            ('results_parent_plan', 'result_id', InstanceType.TEST)
        ]

        for key, parent_key, instance_type in keys:
            file_attachments = await testrail_client.get_attachments_from_list(attachments[key], parent_key)
            await TestyCreator.attachment_bulk_create(file_attachments, project, user, parent_key, mappings[key],
                                                      instance_type)
        if upload_root_runs:
            keys = [
                ('results_parent_mile', 'result_id', InstanceType.TEST),
                ('runs_parent_mile', 'run_id', InstanceType.RUN)
            ]
            for key, parent_key, instance_type in keys:
                file_attachments = await testrail_client.get_attachments_from_list(attachments[key],
                                                                                   parent_key)
                await TestyCreator.attachment_bulk_create(file_attachments, project, user, parent_key, mappings[key],
                                                          instance_type)


@shared_task(bind=True)
def download_task(self, project_id, config_dict, create_dump: bool, dumpfile_path):
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 1, 'Started downloading')

    results = download(project_id, TestrailConfig(**config_dict))

    results_json = json.dumps(results)
    redis_client = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT)

    logging.info(f'REDIS CLIENT PING {redis_client.ping()}')

    backup_name = f'backup{datetime.now()}'
    TestrailBackup.objects.create(name=backup_name, filepath=backup_name)
    redis_client.set(backup_name, results_json)

    if not redis_client.get(backup_name):
        logging.error('REDIS CLIENT GET GOT NOTHING')


@async_to_sync
async def download(project_id: int, config: TestrailConfig, download_attachments: bool = True):
    # TODO: think about processing entries
    async with TestRailClient(config) as testrail_client:
        resulting_data = {'project': await testrail_client.get_project(project_id)}
        resulting_data.update(await testrail_client.download_descriptions(project_id))
        resulting_data.update(await testrail_client.download_representations(project_id))

        if not download_attachments:
            return resulting_data

        keys_instance_type = [
            ('cases', InstanceType.CASE),
            ('plans', InstanceType.PLAN),
            ('runs_parent_mile', InstanceType.RUN),
            ('runs_parent_plan', InstanceType.RUN),
            ('results_parent_plan', InstanceType.TEST),
            ('results_parent_mile', InstanceType.TEST)
        ]

        resulting_data['attachments'] = {}

        for key, instance_type in keys_instance_type:
            resulting_data['attachments'][key] = await testrail_client.get_attachments_for_instances(
                resulting_data[key],
                instance_type
            )
    return resulting_data
