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

def login(request, *args, **kwargs):
    return render(request, 'core/login.html')

def register(request, *args, **kwargs):
    return render(request, 'core/register.html')

def settings(request, *args, **kwargs):
    return render(request, 'core/settings.html', context={"topUsers" : TOPUSERS, "topTags": TOPTAGS})
