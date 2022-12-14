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

from asgiref.sync import async_to_sync
from core.models import Project
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from tests_description.models import TestCase, TestSuite
from tests_representation.models import Parameter, Test, TestPlan, TestResult

from .migrator_lib import TestRailClient, TestrailConfig
from .models import TestrailBackup, TestrailSettings
from .serializers import (
    DownloadSerializer,
    TestrailBackupSerializer,
    TestrailSettingsInputSerializer,
    TestrailSettingsOutputSerializer,
    TestrailUploadSerializer,
)
from .tasks import download_task, upload_task


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

        config_dict = {
            'login': testrail_settings.login,
            'password': testrail_settings.password,
            'api_url': testrail_settings.api_url,
        }
        task = download_task.delay(project_id, config_dict, request.POST.get('create_dumpfile'),
                                   testrail_settings.dumpfile_path)
        return redirect(reverse('plugins:testrail_migrator:download_status', kwargs={'task_id': task.task_id}))


def download_status(request, task_id):
    return render(request, 'download_status.html', {'task_id': task_id})


class UploaderView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = TestrailUploadSerializer

    def create(self, request, *args, **kwargs):
        backup_instance = TestrailBackup.objects.get(pk=request.POST.get('testrail_backup'))
        task = upload_task.delay(backup_instance.name, request.POST.get('user'))
        return redirect(reverse('plugins:testrail_migrator:download_status', kwargs={'task_id': task.task_id}))


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
        TestrailBackup.objects.all().delete()
        TestrailSettings.objects.all().delete()
        return Response('All cleared!')


class Do(APIView):
    def get(self, request):
        self.gather_attachments()

        return Response('123')

    # @async_to_sync
    # async def gather_attachments(self):
    #     config = TestrailConfig(login='r.kabaev', password='Pfchfycbz2022', api_url='http
    #     s://testrail.yadro.com/index.php?/api/v2')
    #     async with TestRailClient(config) as testrail_client:
    #         with open('/Users/r.kabaev/Desktop/testy/backup2022-12-14 12:04:25.813287.json', 'r') as file:
    #             cases = json.loads(file.read())['cases']
    #         attachments = await testrail_client.get_attachments_for_instances(cases, InstanceType.CASE)
    #         with open('/Users/r.kabaev/Desktop/testy/attachments_for_cases.json', 'w') as file:
    #             file.write(json.dumps(attachments, indent=2))
    #     print()

    @async_to_sync
    async def gather_attachments(self):
        config = TestrailConfig(login='r.kabaev', password='Pfchfycbz2022',
                                api_url='https://testrail.yadro.com/index.php?/api/v2')

        # with open('/Users/r.kabaev/Desktop/testy/backup2022-12-14 12:04:25.813287.json', 'r') as file:
        #     backup = json.loads(file.read())

        with open('/Users/r.kabaev/Desktop/testy/attachments_for_cases.json', 'r') as file:
            attachments_cases = json.loads(file.read())

        async with TestRailClient(config) as testrail_client:
            # attachments_cases = await testrail_client.get_attachments
            # _for_instances(backup['cases'], InstanceType.CASE)
            # attachments_runs_plans = await testrail_client.get_attachments_for_instances(backup['runs_parent_plan'],
            #                                                                              InstanceType.RUN)
            # attachments_plans = await testrail_client.get_attachme
            # nts_for_instances(backup['plans'], InstanceType.PLAN)
            # attachments_tests_plans = await testrail_client.get_attachments_for_instances(backup['tests_parent_plan'],
            #                                                                               InstanceType.TEST)
            for attachment in attachments_cases:
                t = await testrail_client.get_attachment(attachment['id'])
                print(t)
        print()
