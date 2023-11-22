from django.urls import path

from chat import consumers


websocket_urlpatterns = [
    path(
        "ws/chats/new_conversation/",
        consumers.NewConversationConsumer.as_asgi()
    ),
]
