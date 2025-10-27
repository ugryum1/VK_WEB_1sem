from django.shortcuts import render

TOPUSERS = [
    {
        "rank": 1,
        "username": "Dr. Pepsi"
    },
    {
        "rank": 2,
        "username": "Secret User"
    },
    {
        "rank": 3,
        "username": "Carte Blanche"
    }
]

TOPTAGS = [
    {
        "id": 1,
        "tag": "Python"
    },
    {
        "id": 2,
        "tag": "PostgreSQL"
    },
    {
        "id": 3,
        "tag": "Django"
    },
    {
        "id": 4,
        "tag": "VK"
    },
    {
        "id": 5,
        "tag": "Mail.ru"
    },
    {
        "id": 6,
        "tag": "Go"
    },
    {
        "id": 7,
        "tag": "C++"
    }
]

QUESTIONS = [
    {
        "id": 1,
        "questionTitle": "Как установить Python на Windows?",
        "questionText": "Подскажите, как правильно установить Python на Windows 10. Нужно ли скачивать с официального сайта или есть другие способы?",
        "answersCount": 10,
        "tags": ["Python", "Windows", "Установка"],
        "username": "Dr. Pepsi",
        "avatar": "/static/questions/img/Dr_Pepsi.png",
        "questionRating": 15
    },
    {
        "id": 2,
        "questionTitle": "Лучшие практики Go для микросервисов",
        "questionText": "Какие архитектурные паттерны и лучшие практики рекомендуются для построения микросервисов на Go?",
        "answersCount": 4,
        "tags": ["Go", "Микросервисы"],
        "username": "Secret User",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 8
    },
    {
        "id": 3,
        "questionTitle": "Как настроить Django с PostgreSQL?",
        "questionText": "Подскажите, как правильно настроить соединение между Django и PostgreSQL на production сервере. Какие лучшие практики? Какие лучшие практики?",
        "answersCount": 3,
        "tags": ["Django", "PostgreSQL", "Python"],
        "username": "Carte Blanche",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 5
    }
]

TAG = [
    {
        "id": 1,
        "questionTitle": "Как настроить Django с PostgreSQL?",
        "questionText": "Подскажите, как правильно настроить соединение между Django и PostgreSQL на production сервере. Какие лучшие практики?",
        "answersCount": 5,
        "tags": ["Django", "PostgreSQL", "Python"],
        "username": "Dr. Pepsi",
        "avatar": "/static/questions/img/Dr_Pepsi.png",
        "questionRating": 15
    },
    {
        "id": 2,
        "questionTitle": "Как развернуть массив?",
        "questionText": "Как развернуть list в Python, не используя встроенные методы списков?",
        "answersCount": 3,
        "tags": ["Python", "Массивы"],
        "username": "Carte Blanche",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 6
    },
    {
        "id": 3,
        "questionTitle": "Как отсортировать список по возрастанию?",
        "questionText": "Как отсортировать список по возрастанию в Python, не используя встроенные методы списков?",
        "answersCount": 2,
        "tags": ["Python", "Сортировки", "Массивы"],
        "username": "Secret User",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 5
    }
]

QUESTION = [
    {
        "id": 1,
        "questionTitle": "Как установить Python на Windows?",
        "questionText": "Подскажите, как правильно установить Python на Windows 10. Нужно ли скачивать с официального сайта или есть другие способы?",
        "answersCount": 10,
        "tags": ["Python", "Windows", "Установка"],
        "username": "Dr. Pepsi",
        "avatar": "/static/questions/img/Dr_Pepsi.png",
        "questionRating": 15
    }
]

ANSWERS = [
    {
        "id": 1,
        "answerText": "Скачайте установщик с официального сайта python.org. Запустите скачанный файл и не забудьте поставить галочку 'Add Python to PATH' во время установки.",
        "username": "Carte Blanche",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 8
    },
    {
        "id": 2,
        "answerText": "Также можно установить через Microsoft Store - это проще для новичков. Просто откройте Microsoft Store, найдите Python и нажмите 'Установить'.",
        "username": "Secret User",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 5
    }
]

def index(request, *args, **kwargs):
    return render(request, 'questions/index.html', context={"questions": QUESTIONS, "topUsers": TOPUSERS, "topTags": TOPTAGS})

def question(request, *args, **kwargs):
    return render(request, 'questions/question.html', context={"questions": QUESTION, "answers": ANSWERS, "topUsers": TOPUSERS, "topTags": TOPTAGS})

def ask(request, *args, **kwargs):
    return render(request, 'questions/ask.html', context={"topUsers": TOPUSERS, "topTags": TOPTAGS})

def tag(request, *args, **kwargs):
    return render(request, 'questions/tag.html', context={"questions": TAG, "topUsers": TOPUSERS, "topTags": TOPTAGS})

# пока что главная страница = странице топовых вопросов, пока не используем данные из БД
def top(request, *args, **kwargs):
    return render(request, 'questions/topQuestions.html', context={"questions": QUESTIONS, "topUsers": TOPUSERS, "topTags": TOPTAGS})
