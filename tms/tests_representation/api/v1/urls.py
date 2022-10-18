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

result_detail = views.TestResultViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'
})

result_list = views.TestResultViewSet.as_view({
    'get': 'list'
})

results_by_test = views.TestResultViewSet.as_view({
    'get': 'results_by_test'
})

add_result_to_test = views.TestResultViewSet.as_view({
    'post': 'add_result'
})

urlpatterns = [
    path('tests/', test_lists, name='test-list'),
    path('tests/<int:pk>/', test_detail, name='test-detail'),
    path('tests/<int:pk>/results/', add_result_to_test, name='result-add'),
    path('tests/<int:pk>/results/', views.TestResultsByTest.as_view(), name='results-by-test'),
    path('results/', result_list, name='result-list'),
    path('results/<int>:pk/', result_detail, name='result-detail'),

]
urlpatterns += router.urls
