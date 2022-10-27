from django.urls import path
from rest_framework.routers import SimpleRouter
from tests_representation.api.v1 import views
from tests_representation.api.v1.views import TestPLanDetailView, TestPLanListView

router = SimpleRouter()
router.register('parameters', views.ParameterViewSet)
router.register('attachments', views.AttachmentViewSet)

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

attachment_list = views.AttachmentViewSet.as_view({
    'get': 'attachments_by_parent'
})

results_by_test = views.TestDetailViewSet.as_view({
    'post': 'add_result',
    'get': 'results_by_test'
})

urlpatterns = [
    path('tests/', test_lists, name='test-list'),
    path('tests/<int:pk>/', test_detail, name='test-detail'),
    path('tests/<int:pk>/results/', results_by_test, name='results-by-test'),

    path('results/', result_list, name='testresult-list'),
    path('results/<int:pk>/', result_detail, name='testresult-detail'),

    path('<str:parent_type>/<int:pk>/attachments/', attachment_list, name='attachments-by-parent')
    path('testplans/', TestPLanListView.as_view(), name='testplan-list'),
    path('testplans/<int:pk>/', TestPLanDetailView.as_view(), name='testplan-detail'),

    path('results/', result_list, name='result-list'),
    path('results/<int>:pk/', result_detail, name='result-detail'),

]
urlpatterns += router.urls
