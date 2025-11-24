from django.shortcuts import render, redirect
from questions.models import Tag
from .models import UserProfile
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import LoginForm
import re


def login(request, *args, **kwargs):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                auth_login(request, user)
                return redirect("questions:main_page")
            else:
                messages.error(request, "Неверный email или пароль")
                return render(request, "core/login.html", context={'form': form})
    else:
        form = LoginForm()

    return render(request, "core/login.html", context={'form': form})


def logout_view(request):
    logout(request)
    return redirect("questions:main_page")


def register(request, *args, **kwargs):
    errors = []

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password_repeat = request.POST.get("password_repeat", "")
        name = request.POST.get("name", "").strip()
        avatar = request.FILES.get("avatar")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                errors.append("Введите корректный email")

        if password != password_repeat:
            errors.append("Пароли должны совпадать")

        if not re.match(r'^[A-Za-z0-9_]+$', password):
            errors.append("Пароль может содержать только английские буквы, цифры и нижнее подчёркивание")

        if len(name) < 3:
            errors.append("Имя должно содержать минимум 3 символа")

        if not re.match(r'^[A-Za-z0-9_]+$', name):
            errors.append("Имя может содержать только английские буквы, цифры и нижнее подчёркивание")

        if User.objects.filter(username=email).exists():
            errors.append("Пользователь с таким email уже существует")

        if UserProfile.objects.filter(name=name).exists():
            errors.append("Имя пользователя уже занято")

        if not errors:
            user = User.objects.create_user(username=email, email=email, password=password)
            profile = UserProfile.objects.create(user=user, name=name)

            if avatar:
                profile.avatar = avatar
                profile.save()

            auth_login(request, user)
            return redirect("questions:main_page")

    return render(request, "core/register.html", context={"errors": errors})


def settings(request, *args, **kwargs):
    top_users = UserProfile.objects.top_users()
    top_tags = Tag.objects.top_tags()

    return render(request, "core/settings.html", context={"top_users": top_users, "top_tags": top_tags})
