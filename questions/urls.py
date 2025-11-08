from django.urls import path

from questions.views import index, question, ask, tag, top

app_name = 'questions'

urlpatterns = [
    path('', index, name='main_page'),
    path('question/<int:question_id>/', question, name='question'),
    path('ask/', ask, name='ask'),
    path('tag/<int:tag_id>/', tag, name='tag'),
    path('hot/', top, name='hot'),
]
