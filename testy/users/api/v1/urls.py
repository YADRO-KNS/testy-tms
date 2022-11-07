
from rest_framework.routers import SimpleRouter
from users.api.v1 import views

router = SimpleRouter()

router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)

urlpatterns = router.urls
