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