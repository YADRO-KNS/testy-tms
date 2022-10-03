from rest_framework import routers

from core.api.v1 import views

router = routers.SimpleRouter()
router.register(r'projects', views.ProjectViewSet)

urlpatterns = router.urls
