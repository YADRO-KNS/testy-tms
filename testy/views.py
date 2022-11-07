
from dataclasses import dataclass

from core.mixins.views import ViewTabMixin
from core.selectors.projects import ProjectSelector
from django.contrib import messages
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import FormView, UpdateView
from forms import ProfilePasswordChangeForm, UserDetailsForm
from tests_representation.selectors.tests import TestSelector
from users.selectors.users import UserSelector
from users.services.users import UserService

from testy.settings.common import LOGIN_REDIRECT_URL

UserModel = get_user_model()

CHANGES_SAVED_SUCCESSFULLY = _('Changes was saved successfully!')


@dataclass
class Tab:
    name: str
    href: str
    args: str = None


class IndexView(View):
    form_class = AuthenticationForm
    auth_template = 'testy/auth.html'
    dashboard_template = 'testy/dashboard.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.auth_template)
        ctx = {}
        ctx['projects'] = ProjectSelector.project_list()
        ctx['users_count'] = UserSelector().user_list().count()
        ctx['tests_count'] = TestSelector().test_list().count()
        return render(request, self.dashboard_template, ctx)

    def post(self, request, *args, **kwargs):
        login_form = self.form_class(request=request, data=request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user())
            return redirect(resolve_url(LOGIN_REDIRECT_URL))
        else:
            return render(request, self.auth_template, {'login_form': login_form})


class UserProfileBaseView(ViewTabMixin):
    tabs = [
        Tab(name='General settings', href='user_profile'),
        Tab(name='Change password', href='user_change_password')
    ]
    template_name = 'testy/user_profile.html'
    success_message = CHANGES_SAVED_SUCCESSFULLY

    def get_object(self, queryset=None):
        return self.request.user


class UserProfileView(UserProfileBaseView, UpdateView):
    model = UserModel
    form_class = UserDetailsForm
    active_tab = 'user_profile'
    success_url = reverse_lazy('user_profile')

    def form_valid(self, form):
        UserService().user_update(user=self.get_object(), data=form.cleaned_data)
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())


class UserChangePasswordView(UserProfileBaseView, FormView):
    form_class = ProfilePasswordChangeForm
    active_tab = 'user_change_password'
    success_url = reverse_lazy('user_change_password')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        UserService().user_update(user=self.get_object(), data={'password': form.cleaned_data['new_password2']})
        update_session_auth_hash(self.request, self.get_object())
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())
