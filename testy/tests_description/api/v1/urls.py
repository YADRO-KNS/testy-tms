
from rest_framework.routers import SimpleRouter
from tests_description.api.v1 import views

router = SimpleRouter()
router.register('cases', views.TestCaseViewSet)
router.register('suites', views.TestSuiteViewSet)

urlpatterns = router.urls
