# -*- encoding: utf-8 -*-
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator, MinLengthValidator, EmailValidator
from main.users.models import User
from django import forms

class SignUpSortForm(forms.Form):
    default_attrs = {'class': 'form-control'}
    email_validators = [
        MaxLengthValidator(limit_value=255, message=_("Maximum length allowed is %(max_length)s") % dict(max_length=255)), 
        MinLengthValidator(limit_value=10, message=_("Minimum length allowed is %(min_length)s") % dict(min_length=10)),
    ]
    password_validators = [
        MaxLengthValidator(limit_value=255, message=_("Maximum length allowed is %(max_length)s") % dict(max_length=255)), 
        MinLengthValidator(limit_value=5, message=_("Minimum length allowed is %(min_length)s") % dict(min_length=5)),
    ]
    email     = forms.CharField(widget=forms.EmailInput(), validators=email_validators, required=True, label=_("Email"))
    password  = forms.CharField(widget=forms.PasswordInput(
        attrs=default_attrs.update(dict(placeholder=_("New Password")))
    ), validators=password_validators, required=True, label=_("Password"))

class SignUpForm(SignUpSortForm):
    first_name_validators = [
        MaxLengthValidator(limit_value=255, message=_("Maximum length allowed is %(max_length)s") % dict(max_length=255)), 
        MinLengthValidator(limit_value=2, message=_("Minimum length allowed is %(min_length)s") % dict(min_length=2)),
    ]
    last_name_validators = [
        MaxLengthValidator(limit_value=255, message=_("Maximum length allowed is %(max_length)s") % dict(max_length=255)), 
        MinLengthValidator(limit_value=2, message=_("Minimum length allowed is %(min_length)s") % dict(min_length=2)),
    ]
    first_name = forms.CharField(widget=forms.TextInput(), validators=first_name_validators, required=True, label=_("First Name"))
    last_name  = forms.CharField(widget=forms.TextInput(), validators=last_name_validators, required=True, label=_("Last Name"))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs=SignUpSortForm.default_attrs.update(dict(placeholder=_("New Password Confirmation")))
    ), validators=SignUpSortForm.password_validators, required=True, label=_("Password Confirmation"))
    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if not password or not password2 or not password == password2:
            self.add_error(field="password2", error=_("The two password fields did not matched."))
        return password
    
    def save(self, commit=True):
        user = super().save(commit=False)  # Call the parent class's save method
        # Generate the username based on the user's name (you can use your custom function here)
        user.username = self.generate_unique_username(self.cleaned_data["first_name"])
        user.is_active = True
        user.is_staff = False

        if commit:
            user.save()
        return user

    def generate_unique_username(self, name):
        # Convert the user's name to a lowercase username with underscores
        base_username = name.lower().replace(" ", "_")

        # Check if the base_username is unique, if not, append a number until it is
        username = base_username
        count = 1
        while User.objects.filter(first_name=username).exists():
            username = f"{base_username}{count}"
            count += 1

        return username