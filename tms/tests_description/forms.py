from crispy_forms.layout import Field, Layout, HTML, Div


from crispy_forms.helper import FormHelper
from django import forms

from tests_description.models import TestCase, TestSuite


class TestCaseForm(forms.ModelForm):

    class Meta:
        model = TestCase
        fields = ('name', 'setup', 'scenario', 'teardown', 'estimate')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'TestCaseCreate'
        self.helper.form_class = 'card border-0 h-100'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Field('name', id='testCaseName', placeholder='Enter name of test case..', css_class="mt-3"),
                HTML(
                    '<button type="button" class="btn btn-sm btn-secondary me-0" style="margin-left: auto;"'
                    'onclick="{{submitAction}}"><i class="bi bi-check"></i></button>'),
                HTML(
                    '<button type="button" class="btn btn-sm btn-secondary ms-1 me-0" onclick="{{cancelAction}}">'
                    '<i class="bi bi-x"></i></button>'),
                css_class='card-header d-flex justify-content-between align-items-center border-3 '
                          'border-light border-bottom', style="height: 60px;"),
            Div(
                Div(
                    HTML(
                        '<div class="card-subtitle border-bottom border-2 border-light" '
                        'style="color: #495057">Estimate</div>'
                    ),
                    Div(
                        Field('estimate', id='estimateTest'), css_class='mx-3 pt-2'),
                    css_class='m-2 mt-4')),
            Div(
                Div(
                    HTML(
                        '<div class="card-subtitle border-bottom border-2 border-light" '
                        'style="color: #495057">Test Setup</div>'
                    ),
                    Div(Field('setup', id='testCaseSetup', rows=3), css_class='mx-3 pt-2'), css_class='m-2 pt-4')),
            Div(
                Div(
                    HTML(
                        '<div class="card-subtitle border-bottom border-2 border-light" '
                        'style="color: #495057">Test Steps</div>'
                    ),
                    Div(Field('scenario', id='testCaseSteps', rows=3), css_class='mx-3 pt-2'), css_class='m-2 pt-4')),
            Div(
                Div(
                    HTML(
                        '<div class="card-subtitle border-bottom border-2 border-light" '
                        'style="color: #495057">Test Teardown</div>'
                    ),
                    Div(Field('teardown', id='testCaseTeardown', rows=3), css_class='mx-3 pt-2'),
                    css_class='m-2 pt-4')),
        )


class TestSuiteForm(forms.ModelForm):

    class Meta:
        model = TestSuite
        fields = ('name', 'parent')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'TestSuiteCreate'
        self.helper.form_class = 'card border-0 h-100'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Field('name', id='testSuiteName', placeholder='Enter name of test suite..', css_class="mt-3"),
                HTML(
                    '<button type="button" class="btn btn-sm btn-secondary me-0" style="margin-left: auto;"'
                    'onclick="{{submitAction}}"><i class="bi bi-check"></i></button>'),
                HTML(
                    '<button type="button" class="btn btn-sm btn-secondary ms-1 me-0" onclick="{{cancelAction}}">'
                    '<i class="bi bi-x"></i></button>'),
                css_class='card-header d-flex justify-content-between align-items-center border-3 '
                          'border-light border-bottom', style="height: 60px;"),
            Div(
                Div(
                    HTML(
                        '<div class="card-subtitle border-bottom border-2 border-light" '
                        'style="color: #495057">Parent suite</div>'
                    ),
                    Div(
                        Field('parent', id='parentTestSuite'), css_class='mx-3 pt-2'),
                    css_class='m-2 mt-4')))
