import json

from core.models import Project
from django.views.generic import DetailView
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
    template_name = 'tms/project/test_suites.html'
    active_tab = 'project_suites'
