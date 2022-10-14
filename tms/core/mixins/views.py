class ViewTabMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tabs'] = self.tabs
        context['active_tab'] = self.active_tab
        return context
