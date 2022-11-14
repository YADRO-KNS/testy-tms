# TestY TMS - Test Management System
# Copyright (C) 2022 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.

from django.urls import path
from rest_framework.routers import SimpleRouter
from tests_representation.api.v1 import views
from tests_representation.api.v1.views import TestPLanDetailView, TestPLanListView, TestResultChoicesView

router = SimpleRouter()
router.register('parameters', views.ParameterViewSet)

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

    path('testplans/', TestPLanListView.as_view(), name='testplan-list'),
    path('testplans/<int:pk>/', TestPLanDetailView.as_view(), name='testplan-detail'),

    path('results/', result_list, name='result-list'),
    path('results/<int>:pk/', result_detail, name='result-detail'),

    path('test-results/', TestResultChoicesView.as_view(), name='test-results'),

]
urlpatterns += router.urls
