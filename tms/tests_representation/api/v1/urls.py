from django.urls import path
from rest_framework.routers import SimpleRouter
from tests_representation.api.v1 import views

router = SimpleRouter()
router.register('parameters', views.ParameterViewSet)
router.register('results', views.TestResultViewSet)

test_lists = views.TestListViewSet.as_view({'get': 'list'})
test_detail = views.TestDetailViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

urlpatterns = [
    path('tests/', test_lists, name='test-list'),
    path('tests/<int:pk>/', test_detail, name='test-detail'),
    path('test_results/<int:test_id>/', views.TestResultByTest.as_view())
]
urlpatterns += router.urls
