from django.shortcuts import render
from questions.models import Tag
from django.contrib.auth.models import User


def login(request, *args, **kwargs):
    return render(request, 'core/login.html')


def register(request, *args, **kwargs):
    return render(request, 'core/register.html')


def settings(request, *args, **kwargs):
    top_users = User.objects.top_users()
    top_tags = Tag.objects.top_tags()

    return render(request, 'core/settings.html', context={"top_users": top_users, "top_tags": top_tags})
