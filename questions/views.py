from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from .models import Question, Answer, Tag, User
from core.models import UserProfile
from django.contrib.auth.models import User

def do_pagination(request, count_per_page, data):
    """ Вспомогательная функция для пагинации """
    paginator = Paginator(data, count_per_page)

    page_number = request.GET.get('page')
    try:
        page_data = paginator.page(page_number)
    except PageNotAnInteger:
        page_data = paginator.page(1)
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages)

    return page_data


def do_pagination(request, count_per_page, data):
    """ Вспомогательная функция для пагинации """
    paginator = Paginator(data, count_per_page)

    page_number = request.GET.get('page')
    try:
        page_data = paginator.page(page_number)
    except PageNotAnInteger:
        page_data = paginator.page(1)
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages)

    return page_data


def get_top_data():
    """ Вспомогательная функция для получения топ данных """
    top_users = UserProfile.objects.top_users()
    top_tags = Tag.objects.top_tags()

    return top_users, top_tags


def index(request, *args, **kwargs):
    top_users, top_tags = get_top_data()
    questions_list = Question.objects.with_related_data()

    page_questions = do_pagination(request, 3, questions_list)

    return render(request, 'questions/index.html',
                  context={"questions": page_questions, "top_users": top_users, "top_tags": top_tags})


def question(request, question_id, *args, **kwargs):
    top_users, top_tags = get_top_data()

    try:
        current_question = Question.objects.with_related_data().get(id=question_id)
    except:
        raise Http404("Вопрос не найден")

    question_answers = Answer.objects.for_question(current_question)

    paginated_answers = do_pagination(request, 2, question_answers)

    return render(request, 'questions/question.html',
                  context={"question": current_question, "answers": paginated_answers,
                           "top_users": top_users, "top_tags": top_tags})


def ask(request, *args, **kwargs):
    top_users, top_tags = get_top_data()
    return render(request, 'questions/ask.html',
                  context={"top_users": top_users, "top_tags": top_tags})


def tag(request, tag_id, *args, **kwargs):
    top_users, top_tags = get_top_data()

    try:
        current_tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        raise Http404("Тег не найден")

    tag_questions = Question.objects.by_tag(current_tag)
    page_questions = do_pagination(request, 3, tag_questions)

    return render(request, 'questions/tag.html',
                  context={"tag": current_tag, "questions": page_questions,
                           "top_users": top_users, "top_tags": top_tags})


def top(request, *args, **kwargs):
    top_users, top_tags = get_top_data()

    questions_list = Question.objects.top_questions()

    page_questions = do_pagination(request, 3, questions_list)

    return render(request, 'questions/top_questions.html',
                  context={"questions": page_questions, "top_users": top_users, "top_tags": top_tags})
