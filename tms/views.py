# TMS - Test Management System
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
from django.views.generic import UpdateView
from django.views.generic.edit import FormView
from forms import ProfilePasswordChangeForm, UserDetailsForm
from users.services.users import UserService

from tms.settings.common import LOGIN_REDIRECT_URL

UserModel = get_user_model()


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


class UserProfileBaseView(ViewTabMixin):
    tabs = {
        'General settings': 'user_profile',
        'Change password': 'user_change_password'
    }
    template_name = 'tms/user_profile.html'
    success_message = _('Changes was saved successfully!')

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
