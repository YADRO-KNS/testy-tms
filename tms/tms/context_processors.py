from django.conf import settings as django_settings


def settings(request):
    """
    Expose Django settings in the template context. Example: {{ settings.VERSION }}
    """
    return {'settings': django_settings}
