from django.urls import include, path
from rest_framework import routers

from tms.api.v1 import views

router = routers.DefaultRouter()
router.APIRootView = views.V1RootView

app_name = 'v1'
urlpatterns = [
    path('', include('core.api.v1.urls')),
    path('', include('tests_description.api.v1.urls')),
    path('', include('tests_representation.api.v1.urls')),
    path('', include('users.api.v1.urls')),
]

urlpatterns += router.urls
