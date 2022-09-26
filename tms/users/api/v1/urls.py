from rest_framework.routers import DefaultRouter
from users.api.v1 import views

router = DefaultRouter()
router.APIRootView = views.UsersRootView

router.register('users', views.UserViewSet)

app_name = 'users-api'
urlpatterns = router.urls
