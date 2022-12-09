# from rest_framework.routers import SimpleRouter
from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import UploaderView, ClearView, TestrailSettingsViewSet, DownloadViewSet, TestrailBackupViewSet

router = SimpleRouter()
router.register('settings', TestrailSettingsViewSet)
router.register('backups', TestrailBackupViewSet)
urlpatterns = [
    path('upload/', UploaderView.as_view({'post': 'create'}), name='name'),
    path('clear/', ClearView.as_view(), name='name'),
    path('download/', DownloadViewSet.as_view({'post': 'create'}))
]
urlpatterns += router.urls
