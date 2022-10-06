from core.api.v1 import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'projects', views.ProjectViewSet)

urlpatterns = router.urls
