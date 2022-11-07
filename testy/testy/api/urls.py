
from django.urls import include, path

from testy.api.views import APIRootView

app_name = 'api'
urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('v1/', include('testy.api.v1.urls', namespace='v1')),
]
