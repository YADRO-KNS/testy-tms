# from rest_framework.routers import SimpleRouter
#
# from testrail_migrator.views import UploaderView
#
# router = SimpleRouter()
#
# router.register('start', UploaderView.as_view())
#
# urlpatterns = router.urls
from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import UploaderView, ClearView
from tests_representation.api.v1.views import ParameterViewSet

# router = SimpleRouter()
#
# router.register('netbb', ParameterViewSet)

urlpatterns = [
    path('start/', UploaderView.as_view(), name='name'),
    path('clear/', ClearView.as_view(), name='name'),
]
