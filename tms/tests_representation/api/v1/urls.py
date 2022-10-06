from rest_framework.routers import SimpleRouter

from tests_representation.api.v1.views import (ParameterViewSet,
                                               TestResultViewSet,
                                               TestStatusViewSet, TestViewSet)

router = SimpleRouter()
router.register('parameters', ParameterViewSet)
router.register('tests', TestViewSet)
router.register('results', TestResultViewSet)
router.register('statuses', TestStatusViewSet)

urlpatterns = router.urls
