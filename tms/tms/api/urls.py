from django.urls import include, path

from tms.api.views import APIRootView

app_name = 'api'
urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('v1/', include('tms.api.v1.urls', namespace='v1')),
]
