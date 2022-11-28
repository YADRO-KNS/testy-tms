import os
import time
from hashlib import md5


def get_attachments_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f'{md5(str(time.time()).encode()).hexdigest()}{extension}'
    return f'attachments/{filename[0:2]}/{filename}'
