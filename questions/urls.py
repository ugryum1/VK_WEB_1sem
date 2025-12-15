from django.urls import path

from questions.views import index, question, ask, tag, top, question_vote, answer_vote, accept_answer

app_name = 'questions'

urlpatterns = [
    path('', index, name='main_page'),
    path('question/<int:question_id>/', question, name='question'),
    path('ask/', ask, name='ask'),
    path('tag/<int:tag_id>/', tag, name='tag'),
    path('hot/', top, name='hot'),
    path('question/<int:question_id>/like/', question_vote, name='question_vote'),
    path('answer/<int:answer_id>/like/', answer_vote, name='answer_vote'),
    path('answer/<int:answer_id>/accept/', accept_answer, name='accept_answer'),
]
