from core.selectors.projects import ProjectSelector


class ViewTabMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tabs'] = self.tabs
        context['active_tab'] = self.active_tab
        return context


class ParameterMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = ProjectSelector.project_by_id(self.kwargs.get('project_id'))
        return context
