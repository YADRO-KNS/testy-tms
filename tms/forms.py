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

from crispy_forms.bootstrap import FormActions, UneditableField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

UserModel = get_user_model()


class UserDetailsForm(forms.ModelForm):
    username = forms.CharField(disabled=True)

    class Meta:
        model = UserModel
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
            Div(
                Div(
                    Div(UneditableField('username', css_class='form-control', help_text=None), css_class='row'),
                    Div('first_name', css_class='row'),
                    Div('last_name', css_class='row'),
                    Div('email', css_class='row'),
                    css_class="col-md-6"
                ),
                css_class="row justify-content-start"
            ),
            HTML('<hr class="mt-0">'),
            FormActions(
                Submit('Save', 'Save changes', css_class='btn-primary'),
            ),
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
            Div(
                Div(
                    Div('old_password', css_class='row'),
                    Div('new_password1', css_class='row'),
                    Div('new_password2', css_class='row'),
                    css_class="col-md-6"
                ),
                css_class="row justify-content-start"
            ),
            HTML('<hr class="mt-0">'),
            FormActions(Submit('Save', 'Change password', css_class='btn-primary'), css_class='mb-0')
        )
