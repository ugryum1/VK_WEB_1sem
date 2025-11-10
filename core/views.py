from django.shortcuts import render
from fictional_data import TOPUSERS, TAGS


def login(request, *args, **kwargs):
    return render(request, 'core/login.html')


def register(request, *args, **kwargs):
    return render(request, 'core/register.html')


def settings(request, *args, **kwargs):
    return render(request, 'core/settings.html', context={"top_users": TOPUSERS, "top_tags": TAGS})
