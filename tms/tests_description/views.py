from crispy_forms.utils import render_crispy_form
from django.db.models import QuerySet
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import UpdateView, CreateView, DeleteView

from core.models import Project
from core.selectors.projects import ProjectSelector
from tests_description.forms import TestCaseForm, TestSuiteForm
from tests_description.models import TestCase, TestSuite
from tests_description.selectors.cases import TestCaseSelector
from tests_description.selectors.suites import TestSuiteSelector
from tests_description.services.cases import TestCaseService
from tests_description.services.suites import TestSuiteService


class TestCaseView(View):
    model = TestCase
    template_name = 'tms/project/suites/test_case_description.html'

    def get(self, request, *args, **kwargs):
        test_case_id = request.GET['test_case_id']
        test_case = TestCaseSelector().case(test_case_id)
        return JsonResponse({'test_template': render_to_string(self.template_name, {'test_case': test_case})})


class TestCaseEditView(UpdateView):
    model = TestCase
    form_class = TestCaseForm
    template_name = "tms/project/suites/test_case_description.html"

    def get(self, request, *args, **kwargs):
        test_case_id = request.GET['test_case_id']
        test_case = TestCaseSelector().case(test_case_id)
        form = TestCaseForm(instance=test_case)
        html = render_crispy_form(form, context={'submitAction': f"saveTestCase({test_case.pk})",
                                                 'cancelAction': f"getTestDescription({test_case.pk})"})
        return JsonResponse({'test_template': html})

    def post(self, request, *args, **kwargs):
        test_case_id = request.POST.get('id')
        test_case = TestCaseSelector().case(test_case_id)
        data = {
            'name': request.POST.get('name'),
            'setup': request.POST.get('setup'),
            'scenario': request.POST.get('scenario'),
            'teardown': request.POST.get('teardown'),
            'estimate': request.POST.get('estimate'),
        }
        form = TestCaseForm(request.POST, initial=data)
        test_suite = TestSuiteSelector().suite(name=test_case.suite)
        if form.is_valid():
            test_case = TestCaseService().case_update(case=test_case, data=data)
            return JsonResponse({'test_template': render_to_string(self.template_name, {'test_case': test_case}),
                                 'test_suite_id': test_suite.pk})
        return JsonResponse(
            {'test_template': render_crispy_form(form, context={'submitAction': f"saveTestCase({test_case.pk})",
                                                                'cancelAction': f"getTestDescription({test_case.pk})"})}
        )


class TestCaseCreateView(CreateView):
    model = TestCase
    form_class = TestCaseForm
    template_name = "tms/project/suites/test_case_description.html"

    def get(self, request, *args, **kwargs):
        test_suite_id = request.GET['test_suite_id']
        test_suite = TestSuiteSelector().suite(pk=test_suite_id)
        html = render_crispy_form(TestCaseForm(),
                                  context={'test_suite': test_suite,
                                           'submitAction': f"addTestCase({test_suite.pk},'{test_suite.project}')",
                                           'cancelAction': "closeTestCase()"})
        return JsonResponse({'test_template': html})

    def post(self, request, *args, **kwargs):
        request_params = request.POST
        suite_name = request_params.get('suite')
        project = request_params.get('project')
        suite_model = QuerySet(model=TestSuite).filter(id=suite_name)[0]
        project_model = QuerySet(model=Project).filter(name=project)[0]
        data = {
            'suite': suite_model,
            'scenario': request_params.get('scenario'),
            'project': project_model,
            'name': request.POST.get('name'),
            'setup': request.POST.get('setup'),
            'teardown': request_params.get('teardown'),
            'estimate': request_params.get('estimate'),
        }
        form = TestCaseForm(request.POST, initial=data)
        if form.is_valid():
            test_case = TestCaseService().case_create(data=data)
            return JsonResponse({'test_template': render_to_string(self.template_name, {'test_case': test_case})})
        return JsonResponse(
            {'test_template': render_crispy_form(
                form, context={'submitAction': f"addTestCase({suite_model.pk},'{suite_model.project}')",
                               'cancelAction': "closeTestCase()"})})


class TestCaseDeleteView(DeleteView):
    model = TestCase
    active_tab = 'admin_projects'

    def get(self, request, *args, **kwargs):
        test_case_id = request.GET.get('id')
        test_case = TestCaseSelector().case(test_case_id)
        test_case.delete()
        return JsonResponse({'deleted': True, 'test_suite_id': test_case.suite.id})


class TestSuiteView(View):
    model = TestCase
    template_name = 'tms/project/suites/suite_description.html'

    def get(self, request, *args, **kwargs):
        suite_id = request.GET['suite_id']
        suite_name = TestSuiteSelector().suite(pk=suite_id)
        queryset = TestCaseSelector().case_list_for_suite(suite_id)
        return JsonResponse({'cases_list': render_to_string(self.template_name, {'test_cases': queryset,
                                                                                 'test_suite': suite_name})})


class TestSuiteDeleteView(DeleteView):
    model = TestSuite
    active_tab = 'admin_projects'

    def get(self, request, *args, **kwargs):
        test_suite_id = request.GET.get('id')
        test_suite = TestSuiteSelector().suite(pk=test_suite_id)
        test_suite.delete()
        return JsonResponse({'deleted': True})


class TestSuiteCreateView(CreateView):
    model = TestSuite
    form_class = TestSuiteForm
    template_name = "tms/project/suites/suite_description.html"

    def get(self, request, *args, **kwargs):
        form = TestSuiteForm()
        project_id = request.GET['project_id']
        html = render_crispy_form(form, context={'submitAction': f"addTestSuite({project_id})",
                                                 'cancelAction': "closeTestSuite()"})
        return JsonResponse({'test_template': html})

    def post(self, request, *args, **kwargs):
        request_params = request.POST
        suite_name = request_params.get('name')
        parent_suite = request_params.get('parent')
        project_id = request_params.get('project_id')

        data = {
            'name': suite_name,
            'project': ProjectSelector().project(project_id)
        }
        if parent_suite:
            data['parent'] = TestSuiteSelector().suite(pk=parent_suite)

        form = TestSuiteForm(request.POST, initial=data)
        if form.is_valid():
            test_suite = TestSuiteService().suite_create(data=data)
            return JsonResponse({'test_template': render_to_string(self.template_name, {'test_suite': test_suite}),
                                 'test_suite_id': test_suite.pk, 'project_id': project_id})
        return JsonResponse(
            {'test_template': render_crispy_form(
                form, context={'submitAction': f"addTestSuite({project_id})",
                               'cancelAction': "closeTestSuite()"})})
