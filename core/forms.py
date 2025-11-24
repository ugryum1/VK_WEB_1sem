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
            "class": "form-input",
            "placeholder": "Введите пароль",
            "id": "login-password"
        })
    )


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            try:
                user_obj = User.objects.get(email=email)
                if not user_obj.check_password(password):
                    raise ValidationError("Неверный email или пароль")
            except User.DoesNotExist:
                raise ValidationError("Неверный email или пароль")

        return cleaned_data


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label="Логин",
        widget=forms.EmailInput(attrs={
            "class": "form-input",
            "placeholder": "Введите email",
            "id": "reg-login"
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Придумайте пароль",
            "id": "reg-password"
        })
    )
    password_repeat = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Повторите пароль",
            "id": "reg-password-repeat"
        })
    )
    name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Ваше имя",
            "id": "reg-name",
            "minlength": "3"
        })
    )
    avatar = forms.ImageField(
        label="Аватар",
        required=False,
        widget=forms.FileInput(attrs={
            "class": "avatar-input",
            "accept": "image/*",
            "id": "avatar"
        })
    )


    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(username=email).exists():
            raise ValidationError("Пользователь с таким email уже существует")

        return email


    def clean_name(self):
        name = self.cleaned_data["name"]

        if len(name) < 3:
            raise ValidationError("Имя должно содержать минимум 3 символа")

        if not re.match(r'^[A-Za-z0-9_]+$', name):
            raise ValidationError("Имя может содержать только английские буквы, цифры и нижнее подчёркивание")

        if UserProfile.objects.filter(name=name).exists():
            raise ValidationError("Имя пользователя уже занято")

        return name


    def clean_password(self):
        password = self.cleaned_data["password"]

        if not re.match(r'^[A-Za-z0-9_]+$', password):
            raise ValidationError("Пароль может содержать только английские буквы, цифры и нижнее подчёркивание")

        return password


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password and password_repeat and password != password_repeat:
            raise ValidationError("Пароли должны совпадать")

        return cleaned_data


    def save(self):
        email = self.cleaned_data["email"]
        name = self.cleaned_data["name"]
        password = self.cleaned_data["password"]
        avatar = self.cleaned_data.get('avatar')

        user = User.objects.create_user(username=email, email=email, password=password)
        profile = UserProfile.objects.create(user=user, name=name)

        if avatar:
            profile.avatar = avatar
            profile.save()

        return user
