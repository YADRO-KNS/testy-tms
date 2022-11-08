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
from administration import views as administration_views
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path('', login_required(administration_views.AdministrationOverviewView.as_view()), name='admin_overview'),

    # Administration -> Project
    path('projects/', login_required(administration_views.AdministrationProjectsView.as_view()),
         name='admin_projects'),
    path('projects/add/',
         login_required(administration_views.AdministrationProjectsCreateView.as_view()),
         name='admin_project_add'),
    path('projects/<int:pk>/edit/', login_required(administration_views.AdministrationProjectsUpdateView.as_view()),
         name='admin_project_edit'),
    path('projects/<int:pk>/delete/', login_required(administration_views.AdministrationProjectsDeleteView.as_view()),
         name='admin_project_delete'),

    # Administration -> Parameters
    path('projects/<int:project_id>/parameters/add/',
         login_required(administration_views.AdministrationParametersCreateView.as_view()),
         name='admin_parameter_from_project'),
    path('projects/<int:project_id>/edit/parameters/<int:pk>/edit/',
         login_required(administration_views.AdministrationParametersUpdateView.as_view()),
         name='admin_parameter_edit'),
    path('projects/<int:project_id>/parameters/<int:pk>/delete/',
         login_required(administration_views.AdministrationParameterDeleteView.as_view()),
         name='admin_parameter_delete'),

    # Administration -> User
    path('users/', login_required(administration_views.AdministrationUsersView.as_view()), name='admin_users'),
    path('users/add/', login_required(administration_views.AdministrationUserAddView.as_view()),
         name='admin_new_user'),
    path('users/<int:pk>/', login_required(administration_views.AdministrationUserProfileView.as_view()),
         name='admin_user_profile'),
    path('users/<int:pk>/delete/',
         login_required(administration_views.AdministrationUserDeleteView.as_view()), name='admin_user_delete'),
]
