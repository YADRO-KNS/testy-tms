from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()


class UserAddForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-3'
        self.helper.field_class = 'col-8'
        self.helper.form_tag = False
        self.helper.use_custom_control = False
        self.helper.layout = Layout(
            Div('username', css_class='row mb-1'),
            Div('first_name', css_class='row mb-1'),
            Div('last_name', css_class='row mb-1'),
            Div('email', css_class='row mb-1'),
            Div('password1', css_class='row mb-1'),
            Div('password2', css_class='row mb-1'),
            HTML("""<hr class="mt-0">"""),
            FormActions(Submit('Save', 'Add user', css_class='btn-secondary'), css_class='mb-0')
        )
