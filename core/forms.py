from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile
import re


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Логин",
        widget=forms.EmailInput(attrs={
            "class": "form-input",
            "placeholder": "Введите email",
            "id": "login-email"
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите пароль',
            'id': 'login-password'
        })
    )
