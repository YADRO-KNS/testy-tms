import json
from datetime import datetime

from asgiref.sync import async_to_sync
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django.conf import settings

from testrail_migrator.migrator_lib import TestrailConfig, TestRailClient
from testrail_migrator.models import TestrailBackup


@shared_task(bind=True)
def download_task(self, project_id, config_dict, create_dump: bool, dumpfile_path):
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(0, 1, 'Started downloading')
    results = download(project_id, TestrailConfig(**config_dict))
    # if create_dump:
    timestamp = datetime.now()
    filepath = f'{settings.BASE_DIR.parent}/{dumpfile_path}{timestamp}.json'
    TestrailBackup.objects.create(name=timestamp, filepath=filepath)
    with open(filepath, 'w') as file:
        file.write(json.dumps(results, indent=2))


@async_to_sync
async def download(project_id: int, config: TestrailConfig):
    async with TestRailClient(config) as testrail_client:
        resulting_data = {'project': await testrail_client.get_project(project_id)}
        # resulting_data.update(await testrail_client.download_descriptions(project_id))
        # resulting_data.update(await testrail_client.download_representations(project_id))
    return resulting_data
