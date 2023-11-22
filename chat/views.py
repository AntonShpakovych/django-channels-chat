from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, "chat/index.html")


def search_user(request, username: str):
    users_username = get_user_model().objects.filter(
        username__icontains=username
    )

    return JsonResponse({"users": users_username})
