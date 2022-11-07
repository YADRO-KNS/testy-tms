
from core.api.v1 import views
from django.urls import path
from rest_framework import routers

router = routers.SimpleRouter()

project_list = views.ProjectViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
project_detail = views.ProjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

suites_by_project = views.ProjectViewSet.as_view({
    'get': 'suites_by_project'
})

testplans_by_project = views.ProjectViewSet.as_view({
    'get': 'testplans_by_project'
})

parameters_by_project = views.ProjectViewSet.as_view({
    'get': 'parameters_by_project'
})

urlpatterns = [
    path('projects/', project_list, name='project-list'),
    path('projects/<int:pk>/', project_detail, name='project-detail'),
    path('projects/<int:pk>/suites/', suites_by_project, name='project-suites'),
    path('projects/<int:pk>/testplans/', testplans_by_project, name='project-testplans'),
    path('projects/<int:pk>/parameters/', parameters_by_project, name='project-parameters'),
]

urlpatterns += router.urls
