from django.urls import path

from core.views import login, register, settings

app_name = 'core'

urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', register, name='signup'),
    path('settings/', settings, name='settings'),
]
