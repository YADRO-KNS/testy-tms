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
from typing import Dict

import redis
from asgiref.sync import async_to_sync
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django.conf import settings
from testrail_migrator.migrator_lib import TestRailClient, TestrailConfig, TestyCreator
from testrail_migrator.migrator_lib.testrail import InstanceType
from testrail_migrator.migrator_lib.testy import ParentType
from testrail_migrator.models import TestrailBackup
from tests_description.models import TestCase
from tests_description.services.cases import TestCaseService
from tests_representation.models import TestResult
from tests_representation.services.results import TestResultService


# TODO: переделать чтобы соблюдался принцип DRY
@shared_task(bind=True)
def upload_task(self, backup_name, config_dict, upload_root_runs: bool, service_user_login='admin',
                testy_attachment_url: bool = None):
    progress_recorder = ProgressRecorder(self)

    curr_progress = 0
    max_progress = 14

    progress_recorder.set_progress(curr_progress, max_progress, 'Started uploading')

    redis_client = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT)
    backup = json.loads(redis_client.get(backup_name))
    creator = TestyCreator(service_user_login, testy_attachment_url)

    mappings = {}

    project = creator.create_project(backup['project'])
    mappings['users'] = creator.create_users(backup['users'])
    keys_without_mappings = ['suites', 'configs', 'milestones']
    for key in keys_without_mappings:
        curr_progress += 1
        create_method = getattr(creator, f'create_{key}')
        progress_recorder.set_progress(curr_progress, max_progress, f'Uploading {key}')
        mappings[key] = create_method(backup[key], project.id)

    keys_with_single_mapping = [('sections', 'suites'), ('plans', 'milestones')]
    for key, mapping_key in keys_with_single_mapping:
        curr_progress += 1
        create_method = getattr(creator, f'create_{key}')
        progress_recorder.set_progress(curr_progress, max_progress, f'Uploading {key}')
        mappings[key] = create_method(backup[key], mappings[mapping_key], project.id)

    mappings['cases'] = creator.create_cases(backup['cases'], mappings['suites'], mappings['sections'], project.id)

    mappings['tests_parent_plan'], mappings['runs_parent_plan'] = creator.create_runs(
        runs=backup['runs_parent_plan'],
        mapping=mappings['plans'],
        config_mappings=mappings['configs'],
        tests=backup['tests_parent_plan'],
        case_mappings=mappings['cases'],
        project_id=project.id,
        upload_root_runs=upload_root_runs,
        parent_type=ParentType.PLAN,
        user_mappings=mappings['users']
    )
    curr_progress += 1
    progress_recorder.set_progress(curr_progress, max_progress, 'Uploading tests')
    mappings['results_parent_plan'] = creator.create_results(backup['results_parent_plan'],
                                                             mappings['tests_parent_plan'],
                                                             mappings['users'])
    curr_progress += 1
    progress_recorder.set_progress(curr_progress, max_progress, 'Uploading runs with milestone parent')
    mappings['tests_parent_mile'], mappings['runs_parent_mile'] = creator.create_runs(
        runs=backup['runs_parent_mile'],
        mapping=mappings['milestones'],
        config_mappings=mappings['configs'],
        tests=backup['tests_parent_mile'],
        case_mappings=mappings['cases'],
        project_id=project.id,
        upload_root_runs=upload_root_runs,
        parent_type=ParentType.MILESTONE,
        user_mappings=mappings['users']
    )
    curr_progress += 1
    progress_recorder.set_progress(curr_progress, max_progress, 'Creating results for runs with milestone parent')
    mappings['results_parent_mile'] = creator.create_results(
        backup['results_parent_mile'],
        mappings['tests_parent_mile'],
        mappings['users'],
    )
    mappings['attachments'] = {}
    keys = [
        ('cases', 'case_id', InstanceType.CASE),
        ('plans', 'plan_id', InstanceType.PLAN),
        ('runs_parent_plan', 'run_id', InstanceType.RUN),
        ('runs_parent_mile', 'run_id', InstanceType.RUN),
    ]
    for key, parent_key, instance_type in keys:
        curr_progress += 1
        progress_recorder.set_progress(curr_progress, max_progress, f'Uploading attachments for {key}')
        file_attachments = upload_attachments(config_dict, backup['attachments'][key], parent_key)
        mappings['attachments'].update(
            creator.attachment_bulk_create(file_attachments, project, mappings['users'], parent_key,
                                           mappings[key], instance_type)
        )

    keys = [
        ('parent_plan', 'result_id', InstanceType.TEST),
        ('parent_mile', 'result_id', InstanceType.TEST)
    ]

    for key, parent_key, instance_type in keys:
        curr_progress += 1
        progress_recorder.set_progress(curr_progress, max_progress, f'Uploading attachments for {key}')
        file_attachments = upload_attachments(config_dict, backup['attachments'][f'tests_{key}'], parent_key)
        mappings['attachments'].update(
            creator.attachment_bulk_create(file_attachments, project, mappings['users'], parent_key,
                                           mappings[f'results_{key}'], instance_type)
        )

    logging.info('started uploading attachments')
    mappings_keys = [
        ('cases', TestCase, TestCaseService().case_update, ['scenario', 'setup']),
        ('results_parent_mile', TestResult, TestResultService().result_update, ['comment']),
        ('results_parent_plan', TestResult, TestResultService().result_update, ['comment']),
        # ('milestones', TestPlan, ['description'])
    ]
    for mapping_key, model_class, update_method, field_list in mappings_keys:
        creator.update_testy_attachment_urls(mappings[mapping_key], model_class, update_method, field_list, config_dict)


@async_to_sync
async def upload_attachments(config_dict, attachments, parent_key):
    async with TestRailClient(TestrailConfig(**config_dict)) as testrail_client:
        return await testrail_client.get_attachments_from_list(attachments, parent_key)


@shared_task(bind=True)
def download_task(self, project_id: int, config_dict: Dict, download_attachments, ignore_completed, backup_filename):
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 1, 'Started downloading')

    results = download(project_id, TestrailConfig(**config_dict), download_attachments, ignore_completed)

    results_json = json.dumps(results)
    redis_client = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT)

    logging.info(f'REDIS CLIENT PING {redis_client.ping()}')

    backup_name = f'{backup_filename}{datetime.now()}'
    TestrailBackup.objects.create(name=backup_name, filepath=backup_name)
    redis_client.set(backup_name, results_json)

    if not redis_client.get(backup_name):
        logging.error('REDIS CLIENT GET GOT NOTHING')


@async_to_sync
async def download(project_id: int, config: TestrailConfig, download_attachments: bool, ignore_completed: bool):
    # TODO: think about processing entries
    async with TestRailClient(config) as testrail_client:
        resulting_data = {'project': await testrail_client.get_project(project_id)}
        resulting_data.update(await testrail_client.download_descriptions(project_id))
        resulting_data.update(await testrail_client.download_representations(project_id, ignore_completed))
        resulting_data['users'] = await testrail_client.get_users()
        if not download_attachments:
            return resulting_data

        keys_instance_type = [
            ('cases', InstanceType.CASE),
            ('plans', InstanceType.PLAN),
            ('runs_parent_mile', InstanceType.RUN),
            ('runs_parent_plan', InstanceType.RUN),
            ('tests_parent_mile', InstanceType.TEST),
            ('tests_parent_plan', InstanceType.TEST)
        ]

        resulting_data['attachments'] = {}

        for key, instance_type in keys_instance_type:
            resulting_data['attachments'][key] = await testrail_client.get_attachments_for_instances(
                resulting_data[key],
                instance_type
            )
    return resulting_data
