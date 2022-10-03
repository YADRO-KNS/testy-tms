from rest_framework.routers import SimpleRouter

from tests_representation.api.v1.views import (ParameterViewSet,
                                               TestPlanViewSet,
                                               TestResultViewSet, TestViewSet)

router = SimpleRouter()
router.register('plans', TestPlanViewSet)
router.register('tests', TestViewSet)
router.register('parameters', ParameterViewSet)
router.register('results', TestResultViewSet)

urlpatterns = router.urls
