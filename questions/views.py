from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.db.models import Count
from .models import Question, Answer, Tag, QuestionTag
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


def get_top_data():
    """ Вспомогательная функция для получения топ данных """
    top_users = User.objects.annotate(
        question_count=Count('question')
    ).order_by('-question_count')[:3]

    top_tags = Tag.objects.annotate(
        question_count=Count('questiontag__question')
    ).order_by('-question_count')[:7]

    return top_users, top_tags


def base(request, *args, **kwargs):
    top_users, top_tags = get_top_data()
    return render(request, context={"top_users": top_users, "top_tags": top_tags})


def index(request, *args, **kwargs):
    top_users, top_tags = get_top_data()
    questions_list = Question.objects.all().select_related('user')

    page_questions = do_pagination(request, 3, questions_list)

    return render(request, 'questions/index.html',
                  context={"questions": page_questions, "top_users": top_users, "top_tags": top_tags})


def question(request, question_id, *args, **kwargs):
    top_users, top_tags = get_top_data()

    try:
        current_question = Question.objects.select_related('user').get(id=question_id)
    except:
        raise Http404("Вопрос не найден")

    question_answers = Answer.objects.filter(question=current_question).select_related('user').order_by('-rating')

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

    question_ids = QuestionTag.objects.filter(tag=current_tag).values_list('question_id', flat=True)
    tag_questions = Question.objects.filter(id__in=question_ids).select_related('user').order_by('-rating')

    page_questions = do_pagination(request, 3, tag_questions)

    return render(request, 'questions/tag.html',
                  context={"tag": current_tag, "questions": page_questions,
                           "top_users": top_users, "top_tags": top_tags})


def top(request, *args, **kwargs):
    top_users, top_tags = get_top_data()

    questions_list = Question.objects.all().select_related('user').order_by('-rating')

    page_questions = do_pagination(request, 3, questions_list)

    return render(request, 'questions/top_questions.html',
                  context={"questions": page_questions, "top_users": top_users, "top_tags": top_tags})
