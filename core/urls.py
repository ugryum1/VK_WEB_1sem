from django.urls import path

from core.views import login, register, settings

urlpatterns = [
    path('login/', login),
    path('signup/', register),
    path('settings/', settings),
]
