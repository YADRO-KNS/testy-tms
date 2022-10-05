from rest_framework.routers import SimpleRouter
from tests_representation.api.v1.views import (ParameterViewSet,
                                               TestPlanViewSet,
                                               TestResultViewSet,
                                               TestStatusViewSet, TestViewSet)

router = SimpleRouter()
router.register('plans', TestPlanViewSet)
router.register('tests', TestViewSet)
router.register('parameters', ParameterViewSet)
router.register('results', TestResultViewSet)
router.register('statuses', TestStatusViewSet)

urlpatterns = router.urls
