from django import forms
from .models import User
from django.utils.translation import gettext, gettext_lazy as _

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}),min_length=8)

    confirm_password = forms.CharField(label='Confirm Password (again)',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),min_length=8)

    email = forms.CharField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']
        labels = {'email': 'Email'}

class LoginForm(forms.ModelForm):
    email = forms.EmailField(required=True,widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'password']
        labels = {'email': 'Email'}

class Profile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','locality','city','zipcode']
        widgets = {'name':forms.TextInput(
            attrs={'class':'form-control'}),'locality':forms.TextInput(
                attrs={'class':'form-control'}),'city':forms.TextInput(
                    attrs={'class':'form-control'}),'zipcode':forms.TextInput(
                        attrs={'class':'form-control'})}