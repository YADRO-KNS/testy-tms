from django.conf import settings


def tms_version(request):
    return {'SETTINGS': settings}
