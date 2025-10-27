from django.shortcuts import render

def login(request, *args, **kwargs):
    return render(request, 'core/login.html')

def register(request, *args, **kwargs):
    return render(request, 'core/register.html')

def settings(request, *args, **kwargs):
    return render(request, 'core/settings.html')
