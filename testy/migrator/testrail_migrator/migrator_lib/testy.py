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
import io
import logging
import os
import re
import time
from datetime import datetime
from enum import Enum
from operator import itemgetter

from core.api.v1.serializers import ProjectSerializer
from core.models import Attachment, Project
from core.services.projects import ProjectService
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from testrail_migrator.migrator_lib import TestrailConfig
from testrail_migrator.migrator_lib.testrail import InstanceType, TestrailClientSync
from testrail_migrator.serializers import ParameterSerializer, TestSerializer
from tests_description.api.v1.serializers import TestCaseSerializer, TestSuiteSerializer
from tests_description.models import TestCase
from tests_description.services.cases import TestCaseService
from tests_description.services.suites import TestSuiteService
from tests_representation.api.v1.serializers import TestPlanInputSerializer, TestResultSerializer
from tests_representation.models import TestPlan, TestResult
from tests_representation.services.parameters import ParameterService
from tests_representation.services.results import TestResultService
from tests_representation.services.testplans import TestPlanService
from tests_representation.services.tests import TestService

UserModel = get_user_model()


class ParentType(Enum):
    MILESTONE = 0
    PLAN = 1


class TestyCreator:
    def __init__(self, service_login: str = 'admin',
                 testy_attachment_url: str = None,
                 replace_pattern: str = r'index\.php\?/attachments/get/(?P<attachment_id>\d*)'):
        self.service_user = UserModel.objects.get(username=service_login)
        self.replace_pattern = replace_pattern
        if not testy_attachment_url:
            logging.error('Testy attachment url was not provided')
        self.testy_attachment_url = testy_attachment_url

    def replace_testrail_attachment_url(self, text_to_check, attachments_mapping,
                                        testrail_client: TestrailClientSync, parent_object):
        if not text_to_check:
            return False, text_to_check
        search = re.search(self.replace_pattern, text_to_check)
        if not search:
            return False, text_to_check
        src_attachment_id = int(search.group('attachment_id'))
        attachment_id = attachments_mapping.get(src_attachment_id)
        if not attachment_id:
            file_bytes = testrail_client.get_single_attachment(src_attachment_id)
            temp_file = io.BytesIO(file_bytes)
            name = f'unknown name{time.time()}.png'
            file = InMemoryUploadedFile(
                name=name,
                field_name='file',
                content_type='image/png',
                size=temp_file.__sizeof__(),
                charset='utf-8',
                file=temp_file
            )
            data = {
                'project': parent_object.project,
                'name': name,
                'filename': name,
                'file_extension': 'image/png',
                'size': '123',
                'file': file,
                'user': self.service_user,
                'content_object': parent_object
            }

            attachment = Attachment.objects.create(**data)
            attachment_id = attachment.id

        return True, re.sub(self.replace_pattern, f'{self.testy_attachment_url}{attachment_id}', text_to_check)

    def update_testy_attachment_urls(self, mapping, model_class, update_method, field_list, config_dict):
        testrail_client = TestrailClientSync(TestrailConfig(**config_dict))
        for instance_id in mapping.values():
            data = {}
            instance = model_class.objects.get(pk=instance_id)
            for field in field_list:
                is_replaced, new_instance = self.replace_testrail_attachment_url(
                    getattr(instance, field),
                    mapping,
                    testrail_client,
                    instance
                )
                if not is_replaced:
                    continue
                data[field] = new_instance
            if not data:
                continue
            update_method(instance, data)

    @staticmethod
    def create_suites(suites, project_id):
        suite_data_list = []
        src_ids = []
        for suite in suites:
            src_ids.append(suite['id'])
            suite_data_list.append({'name': suite['name'], 'project': project_id})
        serializer = TestSuiteSerializer(data=suite_data_list, many=True)
        serializer.is_valid(raise_exception=True)
        created_suites = TestSuiteService().suites_bulk_create(serializer.validated_data)

        return dict(zip(src_ids, [created_suite.id for created_suite in created_suites]))

    @staticmethod
    def create_cases(cases, suite_mappings, project_id):
        cases_data_list = []
        src_case_ids = []
        for case in cases:
            src_case_ids.append(case['id'])
            case_data = {
                'name': case['title'],
                'project': project_id,
                'suite': suite_mappings.get(case['suite_id']),
                'scenario': case['custom_steps'],
            }
            setup = case.get('custom_preconds')
            if setup:
                case_data['setup'] = setup
            cases_data_list.append(case_data)
        serializer = TestCaseSerializer(data=cases_data_list, many=True)
        serializer.is_valid(raise_exception=True)
        created_cases = TestCaseService().cases_bulk_create(serializer.validated_data)
        return dict(zip(src_case_ids, [created_case.id for created_case in created_cases]))

    @staticmethod
    def create_configs(config_groups, project_id):
        parameters_mappings = {}
        parameter_data_list = []
        src_config_ids = []
        for config_group in config_groups:
            for config in config_group['configs']:
                src_config_ids.append(config['id'])
                parameter_data = {
                    'group_name': config_group['name'],
                    'data': config['name'],
                    'project': project_id,
                }
                parameter_data_list.append(parameter_data)

        serializer = ParameterSerializer(data=parameter_data_list, many=True)
        serializer.is_valid(raise_exception=True)
        created_parameters = ParameterService().parameter_bulk_create(serializer.validated_data)
        for tr_config_id, testy_parameter in zip(src_config_ids, created_parameters):
            parameters_mappings.update({tr_config_id: testy_parameter.id})

        return parameters_mappings

    @staticmethod
    def create_milestones(milestones, project_id):
        milestones_mapping = {}
        parent_milestones = []
        for milestone in milestones:
            milestone_data = {
                'project': project_id,
                'name': milestone['name'],
                'is_archive': milestone['is_completed'],
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(milestone['started_on'])),
                'finished_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(milestone['completed_on'])),
                'due_date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(milestone['due_on']))
            }
            parent_milestones.append(milestone_data)

        serializer = TestPlanInputSerializer(data=parent_milestones, many=True)
        serializer.is_valid(raise_exception=True)
        test_plans = TestPlanService().testplan_bulk_create(serializer.validated_data)
        for tr_milestone, testy_milestone in zip(milestones, test_plans):
            milestones_mapping.update({tr_milestone['id']: testy_milestone.id})

        for milestone in milestones:
            if not milestone['milestones']:
                continue
            child_milestones_data_list = []
            for child_milestone in milestone['milestones']:
                milestone_data = {
                    'project': project_id,
                    'name': child_milestone['name'],
                    'is_archive': child_milestone['is_completed'],
                    'started_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(milestone['started_on'])),
                    'finished_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(child_milestone['completed_on'])),
                    'due_date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(child_milestone['due_on'])),
                    'parent': milestones_mapping[milestone['id']]
                }
                child_milestones_data_list.append(milestone_data)

            serializer = TestPlanInputSerializer(data=child_milestones_data_list, many=True)
            serializer.is_valid(raise_exception=True)
            test_plans = TestPlanService().testplan_bulk_create(serializer.validated_data)

            for tr_milestone, testy_milestone in zip(milestone['milestones'], test_plans):
                milestones_mapping.update({tr_milestone['id']: testy_milestone.id})

        return milestones_mapping

    @staticmethod
    def create_plans(plans, milestones_mappings, project_id, skip_root_plans: bool = True):
        plan_data_list = []
        plan_mappings = {}
        src_plan_ids = []
        for plan in plans:
            mapping_id = plan['milestone_id']
            if not mapping_id and skip_root_plans:
                continue
            src_plan_ids.append(plan['id'])
            due_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(plan.get('due_on')))
            if not plan.get('due_on'):
                due_date = (datetime.now() + relativedelta(years=5, days=5)).strftime('%Y-%m-%d %H:%M:%S')
            plan_data = {
                'project': project_id,
                'name': plan['name'],
                'is_archive': plan['is_completed'],
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(plan['created_on'])),
                'finished_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(plan['completed_on'])),
                'due_date': due_date,
            }

            if mapping_id:
                plan_data['parent'] = milestones_mappings[mapping_id]
            plan_data_list.append(plan_data)

        serializer = TestPlanInputSerializer(data=plan_data_list, many=True)
        serializer.is_valid(raise_exception=True)
        test_plans = TestPlanService().testplan_bulk_create(serializer.validated_data)
        for src_plan_id, testy_milestone in zip(src_plan_ids, test_plans):
            plan_mappings.update({src_plan_id: testy_milestone.id})

        return plan_mappings

    @staticmethod
    def create_runs(runs, mapping, config_mappings, tests, case_mappings, project_id,
                    parent_type: ParentType, upload_root_runs: bool, user_mappings):
        run_data_list = []
        src_tests = []
        src_run_ids = []
        if parent_type == ParentType.PLAN:
            parent_id_key = 'plan_id'
        elif parent_type == ParentType.MILESTONE:
            parent_id_key = 'milestone_id'
        else:
            raise TypeError('Parent type for test run was not specified')

        for idx, run in enumerate(runs, start=1):
            parent = mapping.get(run[parent_id_key])
            if not parent and not upload_root_runs:
                continue
            src_run_ids.append(run['id'])
            tests_for_run = [test for test in tests if test['run_id'] == run['id']]
            src_tests.extend(tests_for_run)
            cases = [case_mappings[test['case_id']] for test in tests_for_run]
            parameters = [config_mappings[config_id] for config_id in run['config_ids']]
            due_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(run.get('due_on')))
            if not run.get('due_on'):
                due_date = (datetime.now() + relativedelta(years=5, days=5)).strftime('%Y-%m-%d %H:%M:%S')
            run_data = {
                'project': project_id,
                'name': run['name'],
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(run['created_on'])),
                'due_date': due_date,
                'test_cases': cases,
                'parameters': parameters
            }
            if parent:
                run_data['parent'] = parent
            run_data_list.append(run_data)
        serializer = TestPlanInputSerializer(data=run_data_list, many=True)
        serializer.is_valid(raise_exception=True)
        created_tests, created_plans = TestPlanService().testplan_bulk_create_with_tests(serializer.validated_data)

        # Add assignation for tests
        for src_test, created_test in zip(src_tests, created_tests):
            if src_test['assignedto_id']:
                user_id = user_mappings.get(src_test['assignedto_id'])
                TestService().test_update(created_test, {'user': UserModel.objects.get(pk=user_id)})

        return dict(zip(
            [src_test['id'] for src_test in src_tests],
            [created_test.id for created_test in created_tests])
        ), dict(zip(
            src_run_ids,
            [created_plan.id for created_plan in created_plans])
        )

    @staticmethod
    def create_project(project) -> Project:
        data = {
            'name': project['name'],
            'description': project['announcement'] if project['announcement'] else ''
        }
        serializer = ProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return ProjectService().project_create(serializer.validated_data)

    @staticmethod
    def create_tests(tests, case_mappings, plans_mappings, project_id):
        test_data_list = []
        tests_mappings = {}
        src_ids = []
        for test in tests:
            if not case_mappings.get(test['case_id']) or not plans_mappings.get(test['run_id']):
                continue
            src_ids.append(test['id'])
            test_data = {
                'project': project_id,
                'case': case_mappings[test['case_id']],
                'plan': plans_mappings[test['run_id']]
            }
            test_data_list.append(test_data)
        serializer = TestSerializer(data=test_data_list, many=True)
        serializer.is_valid(raise_exception=True)
        created_tests = TestService().tests_bulk_create_by_data_list(serializer.validated_data)
        for src_id, testy_test in zip(src_ids, created_tests):
            tests_mappings.update({src_id: testy_test.id})

        return tests_mappings

    def create_results(self, results, tests_mappings, user_mappings):
        statuses = {
            1: 1,  # passed
            5: 0,  # failed
            8: 2,  # skipped
            2: 4,  # Retest
            3: 5,  # Untested
            4: 3  # Not matching retest in tr / broken in testy
        }
        created_results = []
        src_ids = []
        results = sorted(results, key=itemgetter('created_on'))
        for idx, result in enumerate(results):
            print(f'Processing result {idx} of {len(results)}')
            if not tests_mappings.get(result['test_id']):
                continue
            # Drop all results that serve as assignation message
            if not result['status_id'] and result['assignedto_id']:
                continue
            src_ids.append(result['id'])

            result_data = {
                'status': statuses.get(result['status_id'], 5),
                'comment': result['comment'],
                'test': tests_mappings[result['test_id']],
            }
            user_id = user_mappings.get(result['created_by'])
            user = UserModel.objects.get(pk=user_id) if user_id else self.service_user
            serializer = TestResultSerializer(data=result_data)
            serializer.is_valid(raise_exception=True)
            created_results.append(TestResultService().result_create(serializer.validated_data, user))
        res_ids = [created_result.id for created_result in created_results]
        return dict(zip(src_ids, res_ids))

    def attachment_bulk_create(self, data_dict, project, user_mappings, parent_key, mapping, instance_type):
        non_side_effect_fields = [
            'project', 'name', 'filename', 'comment', 'file_extension', 'content_type', 'size', 'object_id', 'user',
            'file',
            'url'
        ]
        attachment_instances = []
        for data in data_dict.values():
            file = InMemoryUploadedFile(
                name=data['name'],
                field_name='file',
                size=data['size'],
                content_type=data['content_type'],
                charset=data['charset'],
                file=io.BytesIO(data['file_bytes'])
            )
            name, extension = os.path.splitext(file.name)
            user_id = user_mappings.get(data['user_id'])
            temp = {
                'project': project,
                'name': name,
                'filename': file.name,
                'file_extension': file.content_type,
                'size': file.size,
                'file': file,
                'user': UserModel.objects.get(pk=user_id) if user_id else self.service_user
            }
            attachment = Attachment.model_create(fields=non_side_effect_fields, data=temp, commit=False)
            content_object = None
            pk = mapping.get(data[parent_key])
            if instance_type == InstanceType.CASE and pk:
                content_object = TestCase.objects.get(pk=pk)
            elif (instance_type == InstanceType.RUN or instance_type == InstanceType.PLAN) and pk:
                content_object = TestPlan.objects.get(pk=pk)
            elif instance_type == InstanceType.TEST and pk:
                content_object = TestResult.objects.get(pk=pk)
            if content_object:
                attachment.content_object = content_object
            attachment.save()
            attachment_instances.append(attachment)

        return dict(zip(
            [data for data in data_dict],
            [created_attachment.id for created_attachment in attachment_instances])
        )

    @staticmethod
    def user_create(data) -> UserModel:
        non_side_effect_fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']
        user = UserModel.model_create(
            fields=non_side_effect_fields,
            data=data,
            commit=False,
        )
        try:
            user.save()
        except IntegrityError:
            user = UserModel.objects.get(username=data['username'])

        return user

    def create_users(self, users):
        dst_ids = []
        src_ids = []
        for user in users:
            src_ids.append(user['id'])
            user_data = {
                'username': user['email'].split('@')[0],
                'email': user['email'],
                'is_active': user['is_active']
            }
            created_user = self.user_create(user_data)
            dst_ids.append(created_user.id)
        return dict(zip(src_ids, dst_ids))
