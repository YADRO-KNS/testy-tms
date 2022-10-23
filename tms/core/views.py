import json

from core.models import Project
from django.views.generic import DetailView
from tests_description.api.v1.serializers import serializable_object
from tests_description.selectors.suites import TestSuiteSelector
from views import Tab


class ProjectBaseView:
    model = Project
    active_tab = 'project_details'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super(ProjectBaseView, self).get_context_data(**kwargs)
        context['tabs'] = [Tab('Overview', 'project_details', self.kwargs['pk']),
                           Tab('Test Suites & Cases', 'project_suites', self.kwargs['pk']),
                           Tab('Test Plans & Results', 'project_runs', self.kwargs['pk'])]
        context['active_tab'] = self.active_tab
        return context


class ProjectOverviewView(ProjectBaseView, DetailView):
    model = Project
    template_name = 'tms/project/overview.html'


class ProjectPlansView(ProjectBaseView, DetailView):
    model = Project
    template_name = 'tms/project/test_runs.html'
    active_tab = 'project_runs'


class ProjectSuitesView(ProjectBaseView, DetailView):
    model = Project
    template_name = 'tms/project/suites/index.html'
    active_tab = 'project_suites'

    def get_context_data(self, **kwargs):
        context = super(ProjectSuitesView, self).get_context_data(**kwargs)
        root_cases = TestSuiteSelector().suite_project_root_list(self.kwargs['pk'])
        context['treeData'] = []
        for root_case in root_cases:
            context['treeData'].append(serializable_object(root_case))
        context['treeData'] = json.dumps(context['treeData'])
        return context
