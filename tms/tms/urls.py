"""tms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import views
from administration.views import (
    AdministrationNewUserView,
    AdministrationOverviewView,
    AdministrationProjectsCreateView,
    AdministrationProjectsDeleteView,
    AdministrationProjectsUpdateView,
    AdministrationProjectsView,
    AdministrationUserDeleteView,
    AdministrationUserProfileView,
    AdministrationUsersView,
)
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # User profile
    path('user-profile/', login_required(views.UserProfileView.as_view()), name='user_profile'),
    path('user-profile/change-password/', login_required(views.UserChangePasswordView.as_view()),
         name='user_change_password'),

    # Administration
    path('administration/', login_required(AdministrationOverviewView.as_view()), name='admin_overview'),

    # Administration -> Project
    path('administration/projects', login_required(AdministrationProjectsView.as_view()), name='admin_projects'),
    path('administration/projects/add_project', login_required(AdministrationProjectsCreateView.as_view()),
         name='admin_project_add'),
    path('project/<int:pk>/edit', login_required(AdministrationProjectsUpdateView.as_view()),
         name='admin_project_edit'),
    path('administration/projects/<int:pk>/delete', login_required(AdministrationProjectsDeleteView.as_view()),
         name='admin_project_delete'),

    # Administration -> User
    path('administration/users', login_required(AdministrationUsersView.as_view()), name='admin_users'),
    path('administration/users/new_user', login_required(AdministrationNewUserView.as_view()), name='admin_new_user'),
    path('administration/users/<int:pk>', login_required(AdministrationUserProfileView.as_view()),
         name='admin_user_profile'),
    path('administration/users/<int:pk>/delete', login_required(AdministrationUserDeleteView.as_view()),
         name='admin_user_delete'),

    # API
    path('api/', include('tms.api.urls', namespace='api')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Admin
    path('admin/', admin.site.urls),
]
