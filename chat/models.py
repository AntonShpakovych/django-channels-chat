import uuid

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Chat(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    members = models.ManyToManyField(
        User,
        related_name="chats"
    )


class Message(models.Model):
    chat_id = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
