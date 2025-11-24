from django.shortcuts import render, redirect
from questions.models import Tag
from .models import UserProfile
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import LoginForm, RegisterForm
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
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("questions:main_page")
        else:
            for field_errors in form.errors.values():
                errors.extend(field_errors)
    else:
        form = RegisterForm()

    return render(request, "core/register.html", context={"errors": errors})


def settings(request, *args, **kwargs):
    top_users = UserProfile.objects.top_users()
    top_tags = Tag.objects.top_tags()

    return render(request, "core/settings.html", context={"top_users": top_users, "top_tags": top_tags})
