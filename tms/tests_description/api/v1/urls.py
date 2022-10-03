from rest_framework.routers import SimpleRouter
from tests_description.api.v1 import views

router = SimpleRouter()
router.register('suites', views.TestSuiteViewSet)
router.register('cases', views.TestCaseViewSet)

urlpatterns = router.urls
