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
from core.models import Project
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from utilities.request import get_boolean

from .models import TestrailBackup, TestrailSettings
from .serializers import (
    DownloadSerializer,
    TestrailBackupSerializer,
    TestrailSettingsInputSerializer,
    TestrailSettingsOutputSerializer,
    TestrailUploadSerializer,
    TestyDeleteProjectSerializer,
)
from .tasks import download_task, upload_task

UserModel = get_user_model()


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

    def create(self, request, *args, **kwargs):
        project_id = request.POST.get('project_id')
        download_attachments = get_boolean(request, 'download_attachments', 'POST')
        ignore_completed = get_boolean(request, 'ignore_completed', 'POST')
        backup_filename = request.POST.get('backup_filename')

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
        task = download_task.delay(project_id, config_dict, download_attachments, ignore_completed, backup_filename)
        return redirect(reverse('plugins:testrail_migrator:task_status', kwargs={'task_id': task.task_id}))


def task_status(request, task_id):
    return render(request, 'task_status.html', {'task_id': task_id})


class UploaderView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = TestrailUploadSerializer

    def create(self, request, *args, **kwargs):
        backup_instance = TestrailBackup.objects.get(pk=request.POST.get('testrail_backup'))
        upload_root_runs = get_boolean(request, 'upload_root_runs', 'POST')

        try:
            testrail_settings = TestrailSettings.objects.get(pk=request.POST.get('testrail_settings'))
        except TestrailSettings.DoesNotExist:
            return Response('Testrail settings instance were not found', status=status.HTTP_400_BAD_REQUEST)

        config_dict = {
            'login': testrail_settings.login,
            'password': testrail_settings.password,
            'api_url': testrail_settings.api_url,
        }

        task = upload_task.delay(
            backup_name=backup_instance.name,
            config_dict=config_dict,
            testy_attachment_url=testrail_settings.testy_attachments_url,
            upload_root_runs=upload_root_runs
        )
        return redirect(reverse('plugins:testrail_migrator:task_status', kwargs={'task_id': task.task_id}))


class TestyDeleteProjectViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = TestyDeleteProjectSerializer

    def create(self, request, *args, **kwargs):
        Project.objects.get(pk=request.POST.get('testy_project')).delete()
        if get_boolean(request, 'wipe_users', 'POST'):
            UserModel.objects.all().exclude(username='admin').delete()
        return redirect(reverse('plugins:testrail_migrator:delete'))
