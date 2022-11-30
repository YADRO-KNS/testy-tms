from .celery import app as celery_app
from .tasks import process_download

__all__ = (
    'celery_app',
    'process_download'
)
