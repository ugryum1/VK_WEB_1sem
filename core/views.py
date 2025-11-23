from django.shortcuts import render, redirect
from questions.models import Tag
from .models import UserProfile
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages


def login(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("questions:main_page")
        else:
            messages.error(request, "Неверный логин или пароль")

    return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return redirect("questions:main_page")


def register(request, *args, **kwargs):
    return render(request, "core/register.html")


def settings(request, *args, **kwargs):
    top_users = UserProfile.objects.top_users()
    top_tags = Tag.objects.top_tags()

    return render(request, "core/settings.html", context={"top_users": top_users, "top_tags": top_tags})
