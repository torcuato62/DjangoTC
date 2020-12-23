from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from .models import Profile

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control'}))
    class Meta:
        model = User
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

class ProfileForm(forms.ModelForm):
    mostrarNombre = forms.CharField(required=False,
                                    min_length=5,
                                    max_length=20,label='Nombre a mostrar',
                                    widget=forms.TextInput(attrs={'placeholder':'Nombre que mostrará para su usuario'}))
    maxPermisos = forms.ChoiceField(choices=[(x, x) for x in range(0,25,5)],label='Permisos a Mostrar por página')
    class Meta:
        model=Profile
        fields=['mostrarNombre','maxPermisos']
    def clean_mostrarNombre(self):
        return self.cleaned_data['mostrarNombre'] or None


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

