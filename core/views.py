from django.shortcuts import render, redirect
from questions.models import Tag
from .models import UserProfile
from django.contrib.auth import login as auth_login, logout
from .forms import LoginForm, RegisterForm, SettingsForm
from urllib.parse import urlparse, urlunparse


def login(request, *args, **kwargs):
    next_url = request.GET.get("next")

    if not next_url:
        referer = request.META.get("HTTP_REFERER", "")
        if referer and request.get_host() in referer:
            parsed = urlparse(referer)
            clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
            next_url = clean_url
        else:
            next_url = "questions:main_page"

    if '?' in next_url:
        next_url = next_url.split('?')[0]

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            auth_login(request, user)
            return redirect(request.POST.get("next", next_url))
        else:
            return render(request, "core/login.html", context={'form': form, 'next': next_url})
    else:
        form = LoginForm()

    return render(request, "core/login.html", context={'form': form, 'next': next_url})


def logout_view(request):
    referer = request.META.get("HTTP_REFERER", "")

    if not referer and request.get_host() not in next_url:
        next_url = "questions:main_page"
    else:
        special_pages = ['/settings/', '/ask/', '/login/', '/register/']
        is_special_page = any(page in referer for page in special_pages)

        if is_special_page:
            next_url = "questions:main_page"
        else:
            next_url = referer

    logout(request)
    return redirect(next_url)


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
            try:
                user = form.save(request.user)
                if form.cleaned_data.get("new_password"):
                    auth_login(request, user)

                return redirect("core:settings")
            except Exception as e:
                form.add_error(None, f"Ошибка сохранения: {str(e)}")
    else:
        initial_data = { "username" : request.user.username }
        form = SettingsForm(initial=initial_data, user=request.user)


    return render(request, "core/settings.html",
                  context={"top_users": top_users, "top_tags": top_tags, "form": form})
