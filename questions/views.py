from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from fictional_data import TOPUSERS, TAGS, QUESTIONS, ANSWERS

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


def base(request, *args, **kwargs):
    return render(request, context={"top_users": TOPUSERS, "top_tags": TAGS})


def index(request, *args, **kwargs):
    page_questions = do_pagination(request, 3, QUESTIONS)

    return render(request, 'questions/index.html',
                  context={"questions": page_questions, "top_users": TOPUSERS, "top_tags": TAGS})


def question(request, question_id, *args, **kwargs):
    current_question = None
    for question in QUESTIONS:
        if question["id"] == question_id:
            current_question = question
            break

    if not current_question:
        raise Http404("Вопрос не найден")

    question_answers = []
    for answer in ANSWERS:
        if answer.get("question_id") == question_id:
            question_answers.append(answer)

    paginated_answers = do_pagination(request, 2, question_answers)

    return render(request, 'questions/question.html',
                  context={"question": current_question, "answers": paginated_answers,
                           "top_users": TOPUSERS, "top_tags": TAGS})


def ask(request, *args, **kwargs):
    return render(request, 'questions/ask.html',
                  context={"top_users": TOPUSERS, "top_tags": TAGS})


def tag(request, tag_id, *args, **kwargs):
    current_tag = None
    for tag_obj in TAGS:
        if tag_obj["id"] == tag_id:
            current_tag = tag_obj
            break

    if current_tag is None:
        raise Http404("Тег не найден")

    tag_questions = []
    for question in QUESTIONS:
        if current_tag["tag"] in question["tags"]:
            tag_questions.append(question)

    page_questions = do_pagination(request, 3, tag_questions)

    return render(request, 'questions/tag.html',
                  context={"tag": current_tag, "questions": page_questions,
                           "top_users": TOPUSERS, "top_tags": TAGS})


def top(request, *args, **kwargs):
    page_questions = do_pagination(request, 3, sorted(QUESTIONS, key=lambda x: x["question_rating"])[::-1])

    return render(request, 'questions/top_questions.html',
                  context={"questions": page_questions, "top_users": TOPUSERS, "top_tags": TAGS})
