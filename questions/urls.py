from django.urls import path

from questions.views import index, question, ask, tag, top

urlpatterns = [
    path('', index),
    path('question/35/', question),
    path('ask/', ask),
    path('tag/blablabla/', tag),
    path('hot/', top),
]
