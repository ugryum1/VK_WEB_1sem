from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

TAGS = [
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
    },
    {
        "id": 8,
        "tag": "Windows"
    },
    {
        "id": 9,
        "tag": "Установка"
    },
    {
        "id": 10,
        "tag": "Микросервисы"
    }
]

QUESTIONS = [
    {
        "id": 1,
        "questionTitle": "Как установить Python на Windows?",
        "questionText": "Подскажите, как правильно установить Python на Windows 10. Нужно ли скачивать с официального сайта или есть другие способы?",
        "answersCount": 4,
        "tags": ["Python", "Windows", "Установка"],
        "username": "Dr. Pepsi",
        "avatar": "/static/questions/img/Dr_Pepsi.png",
        "questionRating": 15
    },
    {
        "id": 2,
        "questionTitle": "Лучшие практики Go для микросервисов",
        "questionText": "Какие архитектурные паттерны и лучшие практики рекомендуются для построения микросервисов на Go?",
        "answersCount": 3,
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
    },{
        "id": 4,
        "questionTitle": "Как установить Python на Windows?",
        "questionText": "Подскажите, как правильно установить Python на Windows 10. Нужно ли скачивать с официального сайта или есть другие способы?",
        "answersCount": 2,
        "tags": ["Python", "Windows", "Установка"],
        "username": "Dr. Pepsi",
        "avatar": "/static/questions/img/Dr_Pepsi.png",
        "questionRating": 15
    },
    {
        "id": 5,
        "questionTitle": "Лучшие практики Go для микросервисов",
        "questionText": "Какие архитектурные паттерны и лучшие практики рекомендуются для построения микросервисов на Go?",
        "answersCount": 2,
        "tags": ["Go", "Микросервисы"],
        "username": "Secret User",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 8
    },
    {
        "id": 6,
        "questionTitle": "Как настроить Django с PostgreSQL?",
        "questionText": "Подскажите, как правильно настроить соединение между Django и PostgreSQL на production сервере. Какие лучшие практики? Какие лучшие практики?",
        "answersCount": 2,
        "tags": ["Django", "PostgreSQL", "Python"],
        "username": "Carte Blanche",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 5
    },
    {
        "id": 7,
        "questionTitle": "Как установить Python на Windows?",
        "questionText": "Подскажите, как правильно установить Python на Windows 10. Нужно ли скачивать с официального сайта или есть другие способы?",
        "answersCount": 2,
        "tags": ["Python", "Windows", "Установка"],
        "username": "Dr. Pepsi",
        "avatar": "/static/questions/img/Dr_Pepsi.png",
        "questionRating": 15
    },
    {
        "id": 8,
        "questionTitle": "Лучшие практики Go для микросервисов",
        "questionText": "Какие архитектурные паттерны и лучшие практики рекомендуются для построения микросервисов на Go?",
        "answersCount": 2,
        "tags": ["Go", "Микросервисы"],
        "username": "Secret User",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 8
    },
    {
        "id": 9,
        "questionTitle": "Как настроить Django с PostgreSQL?",
        "questionText": "Подскажите, как правильно настроить соединение между Django и PostgreSQL на production сервере. Какие лучшие практики? Какие лучшие практики?",
        "answersCount": 2,
        "tags": ["Django", "PostgreSQL", "Python"],
        "username": "Carte Blanche",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 5
    },
    {
        "id": 10,
        "questionTitle": "Как установить Python на Windows?",
        "questionText": "Подскажите, как правильно установить Python на Windows 10. Нужно ли скачивать с официального сайта или есть другие способы?",
        "answersCount": 1,
        "tags": ["Python", "Windows", "Установка"],
        "username": "Dr. Pepsi",
        "avatar": "/static/questions/img/Dr_Pepsi.png",
        "questionRating": 15
    },
    {
        "id": 11,
        "questionTitle": "Лучшие практики Go для микросервисов",
        "questionText": "Какие архитектурные паттерны и лучшие практики рекомендуются для построения микросервисов на Go?",
        "answersCount": 2,
        "tags": ["Go", "Микросервисы"],
        "username": "Secret User",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 8
    },
    {
        "id": 12,
        "questionTitle": "Как настроить Django с PostgreSQL?",
        "questionText": "Подскажите, как правильно настроить соединение между Django и PostgreSQL на production сервере. Какие лучшие практики? Какие лучшие практики?",
        "answersCount": 1,
        "tags": ["Django", "PostgreSQL", "Python"],
        "username": "Carte Blanche",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 5
    },
    {
        "id": 13,
        "questionTitle": "Как установить Python на Windows?",
        "questionText": "Подскажите, как правильно установить Python на Windows 10. Нужно ли скачивать с официального сайта или есть другие способы?",
        "answersCount": 2,
        "tags": ["Python", "Windows", "Установка"],
        "username": "Dr. Pepsi",
        "avatar": "/static/questions/img/Dr_Pepsi.png",
        "questionRating": 15
    },
    {
        "id": 14,
        "questionTitle": "Лучшие практики Go для микросервисов",
        "questionText": "Какие архитектурные паттерны и лучшие практики рекомендуются для построения микросервисов на Go?",
        "answersCount": 2,
        "tags": ["Go", "Микросервисы"],
        "username": "Secret User",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 8
    },
    {
        "id": 15,
        "questionTitle": "Как настроить Django с PostgreSQL?",
        "questionText": "Подскажите, как правильно настроить соединение между Django и PostgreSQL на production сервере. Какие лучшие практики? Какие лучшие практики?",
        "answersCount": 2,
        "tags": ["Django", "PostgreSQL", "Python"],
        "username": "Carte Blanche",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 5
    },
    {
        "id": 16,
        "questionTitle": "Как установить Python на Windows?",
        "questionText": "Подскажите, как правильно установить Python на Windows 10. Нужно ли скачивать с официального сайта или есть другие способы?",
        "answersCount": 1,
        "tags": ["Python", "Windows", "Установка"],
        "username": "Dr. Pepsi",
        "avatar": "/static/questions/img/Dr_Pepsi.png",
        "questionRating": 15
    },
    {
        "id": 17,
        "questionTitle": "Лучшие практики Go для микросервисов",
        "questionText": "Какие архитектурные паттерны и лучшие практики рекомендуются для построения микросервисов на Go?",
        "answersCount": 2,
        "tags": ["Go", "Микросервисы"],
        "username": "Secret User",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 8
    },
    {
        "id": 18,
        "questionTitle": "Как настроить Django с PostgreSQL?",
        "questionText": "Подскажите, как правильно настроить соединение между Django и PostgreSQL на production сервере. Какие лучшие практики? Какие лучшие практики?",
        "answersCount": 1,
        "tags": ["Django", "PostgreSQL", "Python"],
        "username": "Carte Blanche",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 5
    },
    {
        "id": 19,
        "questionTitle": "Как установить Python на Windows?",
        "questionText": "Подскажите, как правильно установить Python на Windows 10. Нужно ли скачивать с официального сайта или есть другие способы?",
        "answersCount": 2,
        "tags": ["Python", "Windows", "Установка"],
        "username": "Dr. Pepsi",
        "avatar": "/static/questions/img/Dr_Pepsi.png",
        "questionRating": 15
    },
    {
        "id": 20,
        "questionTitle": "Лучшие практики Go для микросервисов",
        "questionText": "Какие архитектурные паттерны и лучшие практики рекомендуются для построения микросервисов на Go?",
        "answersCount": 2,
        "tags": ["Go", "Микросервисы"],
        "username": "Secret User",
        "avatar": "/static/questions/img/anon.png",
        "questionRating": 8
    }
]

ANSWERS = [
    # Ответы на вопрос 1
    {
        "id": 1,
        "question_ID": 1,
        "answerText": "Скачайте установщик с официального сайта python.org. Запустите скачанный файл и не забудьте поставить галочку 'Add Python to PATH' во время установки.",
        "username": "Carte Blanche",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 8
    },
    {
        "id": 2,
        "question_ID": 1,
        "answerText": "Также можно установить через Microsoft Store - это проще для новичков. Просто откройте Microsoft Store, найдите Python и нажмите 'Установить'.",
        "username": "Secret User",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 5
    },
    {
        "id": 3,
        "question_ID": 1,
        "answerText": "Рекомендую использовать pyenv для управления версиями Python, особенно если вы планируете работать с несколькими проектами.",
        "username": "Python Expert",
        "avatar": "/static/questions/img/Dr_Pepsi.png",
        "answerRating": 12
    },
    {
        "id": 4,
        "question_ID": 1,
        "answerText": "После установки проверьте в командной строке: python --version. Должна отобразиться установленная версия.",
        "username": "Tech Helper",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 3
    },

    # Ответы на вопрос 2
    {
        "id": 5,
        "question_ID": 2,
        "answerText": "Используйте goroutine и channels для асинхронной обработки запросов. Это одна из сильных сторон Go.",
        "username": "Go Developer",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 15
    },
    {
        "id": 6,
        "question_ID": 2,
        "answerText": "Рекомендую паттерн hexagonal architecture для лучшей тестируемости и поддерживаемости кода.",
        "username": "Architecture Guru",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 9
    },
    {
        "id": 7,
        "question_ID": 2,
        "answerText": "Не забывайте про graceful shutdown - обрабатывайте сигналы SIGTERM и SIGINT.",
        "username": "DevOps Pro",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 7
    },

    # Ответы на вопрос 3
    {
        "id": 8,
        "question_ID": 3,
        "answerText": "В settings.py укажите DATABASES с правильными параметрами: NAME, USER, PASSWORD, HOST, PORT.",
        "username": "Django Master",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 11
    },
    {
        "id": 9,
        "question_ID": 3,
        "answerText": "Используйте connection pooling с помощью django-db-connections или pgBouncer.",
        "username": "DB Expert",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 6
    },
    {
        "id": 10,
        "question_ID": 3,
        "answerText": "Настройте правильные права доступа для пользователя базы данных в PostgreSQL.",
        "username": "Security First",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 4
    },

    # Ответы на вопрос 4
    {
        "id": 11,
        "question_ID": 4,
        "answerText": "Для Windows рекомендую скачивать с официального сайта, а не использовать сторонние источники.",
        "username": "Security Advisor",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 8
    },
    {
        "id": 12,
        "question_ID": 4,
        "answerText": "Проверьте разрядность вашей системы (32 или 64 бита) перед скачиванием.",
        "username": "Tech Support",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 5
    },

    # Ответы на вопрос 5
    {
        "id": 13,
        "question_ID": 5,
        "answerText": "Используйте context для управления временем жизни запросов и отмены операций.",
        "username": "Go Concurrency",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 10
    },
    {
        "id": 14,
        "question_ID": 5,
        "answerText": "Рекомендую gRPC для межсервисного взаимодействия вместо REST API.",
        "username": "Microservices Fan",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 7
    },

    # Ответы на вопрос 6
    {
        "id": 15,
        "question_ID": 6,
        "answerText": "Настройте миграции Django: python manage.py makemigrations и python manage.py migrate.",
        "username": "Migration Helper",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 9
    },
    {
        "id": 16,
        "question_ID": 6,
        "answerText": "Используйте django-extensions для отладки и разработки.",
        "username": "Django Tools",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 4
    },

    # Ответы на вопрос 7
    {
        "id": 17,
        "question_ID": 7,
        "answerText": "После установки создайте виртуальное окружение: python -m venv myenv.",
        "username": "Virtual Env Pro",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 6
    },
    {
        "id": 18,
        "question_ID": 7,
        "answerText": "Убедитесь, что антивирус не блокирует установку Python.",
        "username": "Troubleshooter",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 3
    },

    # Ответы на вопрос 8
    {
        "id": 19,
        "question_ID": 8,
        "answerText": "Используйте sync.WaitGroup для ожидания завершения группы goroutine.",
        "username": "Concurrency Expert",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 12
    },
    {
        "id": 20,
        "question_ID": 8,
        "answerText": "Настройте мониторинг с помощью Prometheus и Grafana.",
        "username": "Monitoring Guy",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 8
    },

    # Ответы на вопрос 9
    {
        "id": 21,
        "question_ID": 9,
        "answerText": "Для production используйте Gunicorn или uWSGI как WSGI сервер.",
        "username": "Deployment Pro",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 10
    },
    {
        "id": 22,
        "question_ID": 9,
        "answerText": "Настройте кэширование с Redis или Memcached.",
        "username": "Performance Expert",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 7
    },

    # Ответы на вопрос 10
    {
        "id": 23,
        "question_ID": 10,
        "answerText": "Python 3.9+ имеет улучшенную поддержку Windows. Рекомендую последнюю версию.",
        "username": "Version Advisor",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 5
    },

    # Ответы на вопрос 11
    {
        "id": 24,
        "question_ID": 11,
        "answerText": "Используйте структурированное логирование с logrus или zerolog.",
        "username": "Logging Master",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 9
    },
    {
        "id": 25,
        "question_ID": 11,
        "answerText": "Настройте health checks для каждого микросервиса.",
        "username": "Health Checker",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 6
    },

    # Ответы на вопрос 12
    {
        "id": 26,
        "question_ID": 12,
        "answerText": "Используйте django-debug-toolbar для отладки запросов к базе данных.",
        "username": "Debug Helper",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 8
    },

    # Ответы на вопрос 13
    {
        "id": 27,
        "question_ID": 13,
        "answerText": "Для разработки можно использовать IDLE, но лучше PyCharm или VS Code.",
        "username": "IDE Advisor",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 7
    },
    {
        "id": 28,
        "question_ID": 13,
        "answerText": "Установите pip и научитесь управлять пакетами.",
        "username": "Package Manager",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 4
    },

    # Ответы на вопрос 14
    {
        "id": 29,
        "question_ID": 14,
        "answerText": "Используйте docker-compose для оркестрации микросервисов.",
        "username": "Docker Fan",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 11
    },
    {
        "id": 30,
        "question_ID": 14,
        "answerText": "Настройте circuit breaker pattern для устойчивости системы.",
        "username": "Resilience Expert",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 8
    },

    # Ответы на вопрос 15
    {
        "id": 31,
        "question_ID": 15,
        "answerText": "Используйте django-admin для создания административной панели.",
        "username": "Admin Pro",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 6
    },
    {
        "id": 32,
        "question_ID": 15,
        "answerText": "Настройте бэкапы базы данных на регулярной основе.",
        "username": "Backup Master",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 5
    },

    # Ответы на вопрос 16
    {
        "id": 33,
        "question_ID": 16,
        "answerText": "Проверьте совместимость версий Python и вашей ОС.",
        "username": "Compatibility Checker",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 3
    },

    # Ответы на вопрос 17
    {
        "id": 34,
        "question_ID": 17,
        "answerText": "Используйте interface в Go для создания абстракций между сервисами.",
        "username": "Go Architect",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 10
    },
    {
        "id": 35,
        "question_ID": 17,
        "answerText": "Настройте rate limiting для защиты от DDoS атак.",
        "username": "Security Guard",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 7
    },

    # Ответы на вопрос 18
    {
        "id": 36,
        "question_ID": 18,
        "answerText": "Используйте django-cors-headers для настройки CORS если нужен фронтенд.",
        "username": "CORS Expert",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 6
    },

    # Ответы на вопрос 19
    {
        "id": 37,
        "question_ID": 19,
        "answerText": "После установки обновите pip: python -m pip install --upgrade pip.",
        "username": "Pip Updater",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 4
    },
    {
        "id": 38,
        "question_ID": 19,
        "answerText": "Установите необходимые пакеты для вашего проекта через requirements.txt.",
        "username": "Requirements Helper",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 5
    },

    # Ответы на вопрос 20
    {
        "id": 39,
        "question_ID": 20,
        "answerText": "Используйте middleware для сквозной функциональности в микросервисах.",
        "username": "Middleware Master",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 9
    },
    {
        "id": 40,
        "question_ID": 20,
        "answerText": "Настройте distributed tracing с Jaeger или Zipkin.",
        "username": "Tracing Expert",
        "avatar": "/static/questions/img/anon.png",
        "answerRating": 11
    }
]

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

    return render(request, 'questions/index.html', context={"questions": page_questions, "topUsers": TOPUSERS, "topTags": TAGS})

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

    answers_per_page = 3
    paginator = Paginator(question_answers, answers_per_page)

    page_number = request.GET.get('page')
    try:
        paginated_answers = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_answers = paginator.page(1)
    except EmptyPage:
        paginated_answers = paginator.page(paginator.num_pages)

    return render(request, 'questions/question.html', context={"questions": current_question, "answers": paginated_answers, "topUsers": TOPUSERS, "topTags": TAGS})

def ask(request, *args, **kwargs):
    return render(request, 'questions/ask.html', context={"topUsers": TOPUSERS, "topTags": TAGS})

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

    return render(request, 'questions/tag.html', context={"tag": current_tag, "questions": page_questions, "topUsers": TOPUSERS, "topTags": TAGS})

def top(request, *args, **kwargs):
    questions_per_page = 3
    paginator = Paginator(sorted(QUESTIONS, key=lambda x: x["questionRating"])[::-1], questions_per_page)

    page_number = request.GET.get('page')
    try:
        page_questions = paginator.page(page_number)
    except PageNotAnInteger:
        page_questions = paginator.page(1)
    except EmptyPage:
        page_questions = paginator.page(paginator.num_pages)

    return render(request, 'questions/topQuestions.html', context={"questions": page_questions, "topUsers": TOPUSERS, "topTags": TAGS})
