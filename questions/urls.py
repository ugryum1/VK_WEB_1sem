from django.urls import path

from questions.views import index, question, ask, tag, top

app_name = 'questions'

urlpatterns = [
    path('', index, name='main_page'),
    path('question/<int:question_ID>/', question, name='question'),
    path('ask/', ask, name='ask'),
    path('tag/<int:tag_ID>/', tag, name='tag'),
    path('hot/', top, name='hot'),
]
