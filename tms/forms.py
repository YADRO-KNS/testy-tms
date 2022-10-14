from crispy_forms.bootstrap import FormActions, UneditableField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from users.models import User


class UserDetailsForm(forms.ModelForm):
    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        help_texts = {
            'username': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-3'
        self.helper.field_class = 'col-8'
        self.helper.form_tag = False
        self.helper.use_custom_control = False
        self.helper.layout = Layout(
            Div(UneditableField('username', css_class='form-control', help_text=None), css_class='row mb-1'),
            Div('first_name', css_class='row mb-1'),
            Div('last_name', css_class='row mb-1'),
            Div('email', css_class='row mb-1'),
            HTML("""<hr class="mt-0">"""),
            FormActions(
                Submit('Save', 'Save changes', css_class='btn-secondary'),
            )
        )


class ProfilePasswordChangeForm(PasswordChangeForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-4'
        self.helper.field_class = 'col-7'
        self.helper.form_tag = False
        self.helper.use_custom_control = False
        self.helper.layout = Layout(
            Div('old_password', css_class='row mb-1'),
            Div('new_password1', css_class='row mb-1'),
            Div('new_password2', css_class='row mb-1'),
            HTML("""<hr class="mt-0">"""),
            FormActions(
                Submit('Save', 'Change password', css_class='btn-secondary'),
            )
        )