import json

from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.utils.chat_consumer import serialize_contact_data


User = get_user_model()


class FindNewContacts(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        username = data["username"]
        contacts = await self.get_new_contacts_by_username(username=username)

        await self.send(text_data=json.dumps({"contacts": contacts}))

    @database_sync_to_async
    def get_new_contacts_by_username(self, username: str):
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

        excluded_ids.add(self.scope["user"].id)

        user_data = User.objects.filter(
            username__icontains=username
        ).exclude(id__in=excluded_ids).values("username", "is_online")

        serialized_user_data = serialize_contact_data(queryset=user_data)

        return serialized_user_data
