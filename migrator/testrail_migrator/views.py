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

from asgiref.sync import async_to_sync
from core.models import Project
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from tests_description.models import TestCase, TestSuite
from tests_representation.models import Parameter, Test, TestPlan, TestResult

from .migrator_lib import TestRailClient, TestrailConfig
from .migrator_lib.testy import TestyCreator
from .models import TestrailBackup, TestrailSettings
from .serializers import (
    DownloadSerializer,
    TestrailBackupSerializer,
    TestrailSettingsInputSerializer,
    TestrailSettingsOutputSerializer,
    TestrailUploadSerializer,
)


class TestrailSettingsViewSet(ModelViewSet):
    queryset = TestrailSettings.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return TestrailSettingsInputSerializer
        else:
            return TestrailSettingsOutputSerializer


class TestrailBackupViewSet(ModelViewSet):
    serializer_class = TestrailBackupSerializer
    queryset = TestrailBackup.objects.all()


class DownloadViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = DownloadSerializer

    # TODO: add celery
    # TODO: add redis
    def create(self, request, *args, **kwargs):
        project_id = request.POST.get('project_id')

        if not project_id:
            return Response('testrail project id was not specified', status.HTTP_400_BAD_REQUEST)

        try:
            testrail_settings = TestrailSettings.objects.get(pk=request.POST.get('testrail_settings'))
        except TestrailSettings.DoesNotExist:
            return Response('Testrail settings instance were not found', status=status.HTTP_400_BAD_REQUEST)

        config = TestrailConfig(
            login=testrail_settings.login,
            password=testrail_settings.password,
            api_url=testrail_settings.api_url,
        )
        results = self.download(project_id, config)
        if request.POST.get('create_dumpfile'):
            timestamp = datetime.now()
            filepath = f'{settings.BASE_DIR.parent}/{testrail_settings.dumpfile_path}{timestamp}.json'
            testrail_backup = TestrailBackup.objects.create(name=timestamp, filepath=filepath)
            with open(filepath, 'w') as file:
                file.write(json.dumps(results, indent=2))
            return Response(model_to_dict(testrail_backup))
        return Response('Done')

    @staticmethod
    @async_to_sync
    async def download(project_id: int, config: TestrailConfig):
        async with TestRailClient(config) as testrail_client:
            resulting_data = {'project': await testrail_client.get_project(project_id)}
            resulting_data.update(await testrail_client.download_descriptions(project_id))
            resulting_data.update(await testrail_client.download_representations(project_id))
        return resulting_data


class UploaderView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = TestrailUploadSerializer

    def create(self, request, *args, **kwargs):
        # TODO: make backup optional
        user = get_user_model().objects.get(pk=request.POST.get('user'))
        backup_instance = TestrailBackup.objects.get(pk=request.POST.get('testrail_backup'))
        with open(backup_instance.filepath, 'r') as file:
            backup = json.loads(file.read())
        creator = TestyCreator()
        project = creator.create_project(backup['project'])
        logging.info('Project finished')
        suites_mappings = creator.create_suites(backup['suites'], project.id)
        logging.info('Suites finished')
        cases_mappings = creator.create_cases(backup['cases'], suites_mappings, project.id)
        logging.info('Cases finished')
        config_mappings = creator.create_configs(backup['configs'], project.id)
        logging.info('Configs finished')
        milestones_mappings = creator.create_milestones(backup['milestones'], project.id)
        logging.info('milestones_mappings finished')
        plans_mappings = creator.create_plans(backup['plans'], milestones_mappings, project.id)
        logging.info('plans_mappings finished')
        test_mappings = creator.create_runs_parent_plan(
            runs=backup['runs_parent_plan'],
            plan_mappings=plans_mappings,
            config_mappings=config_mappings,
            tests=backup['tests_parent_plan'],
            case_mappings=cases_mappings,
            project_id=project.id
        )
        creator.create_results(backup['results_parent_plan'], test_mappings, user)

        return Response('Done')


# TODO: remove after debugging is finished
class ClearView(APIView):
    def get(self, request):
        Project.objects.all().delete()
        TestPlan.objects.all().delete()
        Test.objects.all().delete()
        TestResult.objects.all().delete()
        TestCase.objects.all().delete()
        TestSuite.objects.all().delete()
        Parameter.objects.all().delete()
        return Response('All cleared!')


class Do(APIView):
    def get(self, request):
        main()
        return Response('All cleared!')


@async_to_sync
async def main():
    config = TestrailConfig(login='r.kabaev', password='Pfchfycbz2022',
                            api_url='https://testrail.yadro.com/index.php?/api/v2')
    client = TestRailClient(config)

    with open('/Users/r.kabaev/Desktop/tms/backup2022-12-09 19:38:08.894586.json', 'r') as file:
        back = json.loads(file.read())
    cases = back['plans']
    for idx, case in enumerate(cases):
        print(f'Case {idx} of {len(cases)}')
        await client.attach(9135)
