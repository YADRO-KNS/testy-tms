import json
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
from tests_representation.api.v1.serializers import TestSerializer
from tests_representation.models import Parameter, Test, TestPlan, TestResult
from tests_representation.selectors.tests import TestSelector
from tests_representation.services.tests import TestService

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
        print('Project finished')
        suites_mappings = creator.create_suites(backup['suites'], project.id)
        print('Suites finished')
        cases_mappings = creator.create_cases(backup['cases'], suites_mappings, project.id)
        print('Cases finished')
        config_mappings = creator.create_configs(backup['configs'], project.id)
        print('Configs finished')
        milestones_mappings = creator.create_milestones(backup['milestones'], project.id)
        print('milestones_mappings finished')
        plans_mappings = creator.create_plans(backup['plans'], milestones_mappings, project.id)
        print('plans_mappings finished')
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
