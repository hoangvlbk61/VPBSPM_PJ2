from django import forms
import re
from .models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user:
                if not self.user.is_active:
                    raise forms.ValidationError("User is Inactive")
            else:
                raise forms.ValidationError("Invalid username and password")
        return self.cleaned_data


class EditProfileForm(forms.ModelForm):

    def clean(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        return self.cleaned_data

    def __init__(self, user, *args, **kwargs):
        # profile_view = kwargs.pop('user', False)
        # self.user = user
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        for key, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.label

        # if profile_view:
        #     self.fields['first_name'].required = True
        #     self.fields['last_name'].required = True
        #     self.fields['email'].required = True

        self.fields['first_name'].widget.attrs.update({
            'value': user.first_name})
        self.fields['last_name'].widget.attrs.update({
            'value': user.last_name})
        self.fields['email'].widget.attrs.update({
            'value': user.email})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=30)
    new_password = forms.CharField(max_length=30)
    new_password_2 = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'new_password_2', ]

    def clean(self):
        old_password = self.cleaned_data.get("old_password")
        new_password = self.cleaned_data.get("new_password")
        new_password_2 = self.cleaned_data.get("new_password_2")
        return self.cleaned_data
