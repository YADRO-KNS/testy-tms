from core.selectors.projects import ProjectSelector
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render, resolve_url
from django.views import View

from tms.settings.common import LOGIN_REDIRECT_URL


class IndexView(View):
    form_class = AuthenticationForm
    auth_template = 'tms/auth.html'
    dashboard_template = 'tms/dashboard.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.auth_template)

        projects = ProjectSelector.project_list()
        return render(request, self.dashboard_template, {'projects': projects})

    def post(self, request, *args, **kwargs):
        login_form = self.form_class(request=request, data=request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user())
            return redirect(resolve_url(LOGIN_REDIRECT_URL))
        else:
            return render(request, self.auth_template, {'login_form': login_form})
