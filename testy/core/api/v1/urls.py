# TestY TMS - Test Management System
# Copyright (C) 2022 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.

from core.api.v1 import views
from django.urls import path
from rest_framework import routers

router = routers.SimpleRouter()

router.register('attachments', views.AttachmentViewSet)

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
