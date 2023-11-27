from django.urls import path

from chat import consumers


websocket_urlpatterns = [
    path(
        "ws/contacts/find/new/",
        consumers.FindNewContacts.as_asgi()
    ),
]
