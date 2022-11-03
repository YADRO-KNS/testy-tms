from administration.forms import UserAddForm
from core.forms import ParameterForm, ProjectForm
from core.mixins.views import ParameterMixin, ViewTabMixin
from core.models import Project
from core.selectors.projects import ProjectSelector
from core.tables import ParameterTable, ProjectTable
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from forms import UserDetailsForm
from tests_representation.models import Parameter
from tests_representation.selectors.parameters import ParameterSelector
from tests_representation.services.parameters import ParameterService
from users.models import User
from users.selectors.users import UserSelector
from users.services.users import UserService
from users.tables import UserTable
from views import CHANGES_SAVED_SUCCESSFULLY, Tab

UserModel = get_user_model()


class AdministrationBaseView:
    tabs = [
        Tab('Overview', 'admin_overview'),
        Tab('Projects', 'admin_projects'),
        Tab('Users', 'admin_users'),
    ]
    success_message = CHANGES_SAVED_SUCCESSFULLY


class AdministrationOverviewView(AdministrationBaseView, ViewTabMixin, View):
    template_name = 'tms/administration/overview.html'
    active_tab = 'admin_overview'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'tabs': self.tabs, 'active_tab': self.active_tab})


class AdministrationProjectsView(AdministrationBaseView, ViewTabMixin, SingleTableMixin, FilterView):
    model = Project
    table_class = ProjectTable
    queryset = ProjectSelector().project_list()
    template_name = 'tms/administration/project/index.html'
    active_tab = 'admin_projects'


class AdministrationUsersView(AdministrationBaseView, ViewTabMixin, SingleTableMixin, FilterView):
    model = User
    table_class = UserTable
    queryset = UserSelector().user_list()
    template_name = 'tms/administration/users/index.html'
    active_tab = 'admin_users'


class AdministrationUserProfileView(AdministrationBaseView, ViewTabMixin, UpdateView):
    model = UserModel
    form_class = UserDetailsForm
    active_tab = 'admin_users'
    template_name = 'tms/administration/users/edit.html'
    success_url = 'admin_users'

    def get_queryset(self):
        return UserSelector().user_list()

    def form_valid(self, form):
        UserService().user_update(user=self.get_object(), data=form.cleaned_data)
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        return reverse('admin_user_profile', kwargs={'pk': self.object.pk})


class AdministrationUserAddView(AdministrationBaseView, ViewTabMixin, CreateView):
    model = User
    form_class = UserAddForm
    template_name = 'tms/administration/users/create.html'
    active_tab = 'admin_users'
    success_url = reverse_lazy('admin_users')


class AdministrationProjectsCreateView(AdministrationBaseView, ViewTabMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tms/administration/project/create.html'
    active_tab = 'admin_projects'
    success_url = reverse_lazy('admin_projects')


class AdministrationProjectsUpdateView(AdministrationBaseView, SingleTableMixin, ViewTabMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tms/administration/project/edit.html'
    active_tab = 'admin_projects'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        qs = ParameterSelector().parameters_by_project_id(context.get('project').id)
        context['parameters_table'] = ParameterTable(qs)
        return context

    def get_success_url(self):
        return reverse('admin_projects')


class AdministrationProjectsDeleteView(AdministrationBaseView, ViewTabMixin, DeleteView):
    model = Project
    template_name = 'tms/administration/confirm_deletion.html'
    active_tab = 'admin_projects'
    success_url = reverse_lazy('admin_projects')
    extra_context = {'href_name': 'admin_projects'}


class AdministrationUserDeleteView(AdministrationBaseView, ViewTabMixin, DeleteView):
    model = User
    template_name = 'tms/administration/confirm_deletion.html'
    active_tab = 'admin_users'
    success_url = reverse_lazy('admin_users')
    extra_context = {'href_name': 'admin_users'}


class AdministrationParameterDeleteView(AdministrationBaseView, ViewTabMixin, ParameterMixin, DeleteView):
    model = Parameter
    template_name = 'tms/administration/confirm_deletion.html'
    active_tab = 'admin_projects'
    extra_context = {'href_name': 'admin_projects'}
    queryset = ParameterSelector().parameter_list()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        success_url = reverse('admin_project_edit', kwargs={'pk': self.kwargs.get('project_id')})
        messages.success(self.request, _('Parameter was deleted successfully!'))
        return HttpResponseRedirect(success_url)


class AdministrationParametersUpdateView(AdministrationBaseView, ViewTabMixin, ParameterMixin, UpdateView):
    model = Parameter
    form_class = ParameterForm
    template_name = 'tms/administration/parameter/edit.html'
    active_tab = 'admin_projects'

    def form_valid(self, form):
        context = self.get_context_data()
        ParameterService().parameter_update(parameter=self.get_object(),
                                            data={'project': context.get('project')} | form.cleaned_data)
        success_url = reverse('admin_project_edit', kwargs={'pk': self.kwargs.get('project_id')})
        messages.success(self.request, _('Parameter was updated successfully!'))
        return HttpResponseRedirect(success_url)


class AdministrationParametersCreateView(AdministrationBaseView, ViewTabMixin, ParameterMixin, CreateView):
    model = Parameter
    form_class = ParameterForm
    template_name = 'tms/administration/parameter/create.html'
    active_tab = 'admin_projects'

    def form_valid(self, form):
        context = self.get_context_data()
        ParameterService().parameter_create(data={'project': context.get('project')} | form.cleaned_data)
        success_url = reverse('admin_project_edit', kwargs={'pk': self.kwargs.get('project_id')})
        messages.success(self.request, _('Parameter was created successfully!'))
        return HttpResponseRedirect(success_url)
