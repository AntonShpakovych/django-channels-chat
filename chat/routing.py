from django.urls import path

from chat import consumers


websocket_urlpatterns = [
    path(
        "ws/contacts/find/new/",
        consumers.FindNewContactsConsumer.as_asgi()
    ),
    path(
        "ws/chats/",
        consumers.ChatListConsumer.as_asgi()
    ),
    path(
        "ws/chats/new/",
        consumers.ChatCreateConsumer.as_asgi()
    ),
    path(
        "ws/chats/<str:chat_id>/",
        consumers.ChatDetailConsumer.as_asgi()
    )
]
