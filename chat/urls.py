from django.urls import path

from chat import views


urlpatterns = [
    path("", views.index, name="chat-list")
]

app_name = "chat"
