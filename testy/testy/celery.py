import asyncio
import os

from asgiref.sync import async_to_sync
from celery import Celery

# Set the default Django settings module for the 'celery' program.
# os.environ.get('DJANGO_SETTINGS_MODULE', 'testy.settings.development')

app = Celery('testy_celery')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    async_to_sync(return_hello)()
    # print(f'Request: {self.request!r}')


async def return_hello():
    await asyncio.sleep(1)
    return 'hello'
