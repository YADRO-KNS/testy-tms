from rest_framework.routers import SimpleRouter
from tests_representation.api.v1.views import (ParameterViewSet,
                                               TestResultViewSet, TestViewSet)

router = SimpleRouter()
router.register('parameters', ParameterViewSet)
router.register('tests', TestViewSet)
router.register('results', TestResultViewSet)

urlpatterns = router.urls
