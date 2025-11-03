from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from fictional_data import TOPUSERS, TAGS, QUESTIONS, ANSWERS

def index(request, *args, **kwargs):
    questions_per_page = 3
    paginator = Paginator(QUESTIONS, questions_per_page)

    page_number = request.GET.get('page')
    try:
        page_questions = paginator.page(page_number)
    except PageNotAnInteger:
        page_questions = paginator.page(1)
    except EmptyPage:
        page_questions = paginator.page(paginator.num_pages)

    return render(request, 'questions/index.html', context={"questions": page_questions, "top_users": TOPUSERS, "top_tags": TAGS})

def question(request, question_ID, *args, **kwargs):
    current_question = []
    for question in QUESTIONS:
        if question["id"] == question_ID:
            current_question.append(question)
            break

    if not current_question:
        from django.http import Http404
        raise Http404("Вопрос не найден")

    question_answers = []
    for answer in ANSWERS:
        if answer.get("question_ID") == question_ID:
            question_answers.append(answer)

    answers_per_page = 2
    paginator = Paginator(question_answers, answers_per_page)

    page_number = request.GET.get('page')
    try:
        paginated_answers = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_answers = paginator.page(1)
    except EmptyPage:
        paginated_answers = paginator.page(paginator.num_pages)

    return render(request, 'questions/question.html', context={"questions": current_question, "answers": paginated_answers, "top_users": TOPUSERS, "top_tags": TAGS})

def ask(request, *args, **kwargs):
    return render(request, 'questions/ask.html', context={"top_users": TOPUSERS, "top_tags": TAGS})

def tag(request, tag_ID, *args, **kwargs):
    current_tag = None
    for tag_obj in TAGS:
        if tag_obj["id"] == tag_ID:
            current_tag = tag_obj
            break

    if current_tag is None:
        from django.http import Http404
        raise Http404("Тег не найден")

    tag_questions = []
    for question in QUESTIONS:
        if current_tag["tag"] in question["tags"]:
            tag_questions.append(question)

    questions_per_page = 3
    paginator = Paginator(tag_questions, questions_per_page)

    page_number = request.GET.get('page')
    try:
        page_questions = paginator.page(page_number)
    except PageNotAnInteger:
        page_questions = paginator.page(1)
    except EmptyPage:
        page_questions = paginator.page(paginator.num_pages)

    return render(request, 'questions/tag.html', context={"tag": current_tag, "questions": page_questions, "top_users": TOPUSERS, "top_tags": TAGS})

def top(request, *args, **kwargs):
    questions_per_page = 3
    paginator = Paginator(sorted(QUESTIONS, key=lambda x: x["question_rating"])[::-1], questions_per_page)

    page_number = request.GET.get('page')
    try:
        page_questions = paginator.page(page_number)
    except PageNotAnInteger:
        page_questions = paginator.page(1)
    except EmptyPage:
        page_questions = paginator.page(paginator.num_pages)

    return render(request, 'questions/top_questions.html', context={"questions": page_questions, "top_users": TOPUSERS, "top_tags": TAGS})
