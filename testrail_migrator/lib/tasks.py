# Celery
from celery import shared_task
# Celery-progress
from celery_progress.backend import ProgressRecorder
# Task imports
import time


# Celery Task
@shared_task(bind=True)
def process_download(self):
    print('Task started')
    # Create the progress recorder instance
    # which we'll use to update the web page
    progress_recorder = ProgressRecorder(self)

    print('Start')
    for i in range(5):
        # Sleep for 1 second
        time.sleep(1)
        # Print progress in Celery task output
        print(i + 1)
        # Update progress on the web page
        progress_recorder.set_progress(i + 1, 5, description="Downloading")
    print('End')

    return 'Task Complete'
