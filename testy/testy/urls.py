
"""testy URL Configuration

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
from core.views import ProjectOverviewView, ProjectPlansView, ProjectSuitesView
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="testy API",
        default_version='v1',
        description="testy API v1",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/', login_required(views.UserProfileView.as_view()), name='user_profile'),
    path('profile/change-password/', login_required(views.UserChangePasswordView.as_view()),
         name='user_change_password'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Administration
    path('administration/', include('administration.urls')),

    # Project
    path('project/<int:pk>/', login_required(ProjectOverviewView.as_view()), name='project_details'),
    path('project/<int:pk>/suites/', login_required(ProjectSuitesView.as_view()), name='project_suites'),
    path('project/<int:pk>/runs/', login_required(ProjectPlansView.as_view()), name='project_runs'),

    # API
    path('api/', include('testy.api.urls', namespace='api')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Admin
    path('admin/', admin.site.urls),

    # Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
