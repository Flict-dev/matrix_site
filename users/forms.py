from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Логин',
            'email': 'Почта',
            'password1': 'Пароль',
            'password2': 'Потверждение пароля'
        }


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        labels = {'email': 'Почта'}
