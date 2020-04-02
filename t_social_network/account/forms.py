from django import forms
from django.contrib.auth.models import User
#from .models import TemporaryRegistrationModel
from .models import UserProfileModel
#import hashlib

class LoginForm (forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationPasswordForm (forms.ModelForm):
    class Meta:
        model = UserProfileModel
        fields = ['user_registration_code']

class UserRegistrationForm (forms.ModelForm):

    password_1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def pasword_validator(self):
        cd = self.cleaned_data
        if cd['password_1'] == cd['password_2']:
            return cd['password_2']
        else:
            return
