import json

from django.contrib.auth import get_user_model
from django.core import serializers

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


User = get_user_model()


class NewConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        username = data["username"]
        users = await self.get_new_users_by_username(username=username)

        await self.send(text_data=json.dumps({"users": users}))

    @database_sync_to_async
    def get_new_users_by_username(self, username: str):
        current_user_with_chats = User.objects.prefetch_related(
            "chats__members"
        ).get(
            id=self.scope["user"].id
        )

        excluded_ids = {
            user.id
            for chat in current_user_with_chats.chats.all()
            for user in chat.members.all()
        }

        return serializers.serialize(
            "json",
            User.objects.filter(
                username__icontains=username
            ).exclude(id__in=excluded_ids),
            fields=["username", "is_online"]
        )
