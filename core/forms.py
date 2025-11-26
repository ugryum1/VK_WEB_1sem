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
                else:
                    cleaned_data["user"] = user_obj
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
    username = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Ваше имя",
            "id": "reg-username",
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

        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует")

        return email


    def clean_username(self):
        username = self.cleaned_data["username"]

        if len(username) < 3:
            raise ValidationError("Имя должно содержать минимум 3 символа")

        if not re.match(r'^[A-Za-z0-9_]+$', username):
            raise ValidationError("Имя может содержать только английские буквы, цифры и нижнее подчёркивание")

        if User.objects.filter(username=username).exists():
            raise ValidationError("Имя пользователя уже занято")

        return username


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
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        avatar = self.cleaned_data.get('avatar')

        user = User.objects.create_user(username=username, email=email, password=password)
        profile = UserProfile.objects.create(user=user)

        if avatar:
            profile.avatar = avatar
            profile.save()

        return user


class SettingsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['username'].initial = self.user.username

    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Ваше имя",
            "id": "username"
        })
    )
    new_password = forms.CharField(
        label="Новый пароль",
        required=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Введите новый пароль",
            "id": "new-password"
        })
    )
    new_password_repeat = forms.CharField(
        label="Повторите новый пароль",
        required=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Повторите новый пароль",
            "id": "new-password-repeat"
        })
    )
    current_password = forms.CharField(
        label="Текущий пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Введите текущий пароль для подтверждения",
            "id": "current-password"
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


    def clean_username(self):
        username = self.cleaned_data["username"]

        if len(username) < 3:
            raise ValidationError("Имя должно содержать минимум 3 символа")

        if not re.match(r'^[A-Za-z0-9_]+$', username):
            raise ValidationError("Имя может содержать только английские буквы, цифры и нижнее подчёркивание")

        if User.objects.filter(username=username).exclude(id=self.user.id).exists():
            raise ValidationError("Имя пользователя уже занято")

        return username


    def clean_current_password(self):
        current_password = self.cleaned_data["current_password"]

        if not self.user.check_password(current_password):
            raise ValidationError("Неверный текущий пароль")

        if not re.match(r'^[A-Za-z0-9_]+$', current_password):
            raise ValidationError("Пароль может содержать только английские буквы, цифры и нижнее подчёркивание")

        return current_password


    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        new_password_repeat = cleaned_data.get("new_password_repeat")

        if new_password and new_password_repeat and new_password != new_password_repeat:
            raise ValidationError("Пароли должны совпадать")

        if new_password and not re.match(r'^[A-Za-z0-9_]+$', new_password):
                raise ValidationError("Пароль может содержать только английские буквы, цифры и нижнее подчёркивание")

        return cleaned_data
