from django.shortcuts import render, redirect
from questions.models import Tag
from .models import UserProfile
from django.contrib.auth import login as auth_login, logout
from .forms import LoginForm, RegisterForm, SettingsForm


def login(request, *args, **kwargs):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            auth_login(request, user)
            return redirect("questions:main_page")
        else:
            return render(request, "core/login.html", context={'form': form})
    else:
        form = LoginForm()

    return render(request, "core/login.html", context={'form': form})


def logout_view(request):
    logout(request)
    return redirect("questions:main_page")


def register(request, *args, **kwargs):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("questions:main_page")
    else:
        form = RegisterForm()

    return render(request, "core/register.html", context={"form": form})


def settings(request, *args, **kwargs):
    top_users = UserProfile.objects.top_users()
    top_tags = Tag.objects.top_tags()

    if request.method == "POST":
        form = SettingsForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            user = request.user
            username = form.cleaned_data["username"]
            new_password = form.cleaned_data.get("new_password")
            avatar = form.cleaned_data.get("avatar")

            if username != user.username:
                user.username = username
                user.save()

            if new_password:
                user.set_password(new_password)
                user.save()
                auth_login(request, user)

            if avatar:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.avatar = avatar
                user_profile.save()

            return redirect("questions:main_page")
        else:
            form = SettingsForm(user=request.user)
    else:
        initial_data = { "username" : request.user.username }
        form = SettingsForm(initial=initial_data, user=request.user)


    return render(request, "core/settings.html",
                  context={"top_users": top_users, "top_tags": top_tags, "form": form})
