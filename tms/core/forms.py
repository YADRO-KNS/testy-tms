from core.models import Project
from crispy_forms.helper import FormHelper
from django import forms
from tests_representation.models import Parameter


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-3'
        self.helper.field_class = 'col-8 row mb-1'
        self.helper.form_tag = False
        self.helper.use_custom_control = False


class ParameterForm(forms.ModelForm):
    class Meta:
        model = Parameter
        fields = ('project', 'group_name', 'data')
        widgets = {
            'project': forms.HiddenInput()
        }

    def __init__(self, *args, pk=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial = {
            'project': pk if pk else self.instance.project,
            'group_name': self.instance.group_name,
            'data': self.instance.data
        }
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-3'
        self.helper.field_class = 'col-8 row mb-1'
        self.helper.form_tag = False
        self.helper.use_custom_control = False
