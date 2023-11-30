import json

from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


from chat.models import Chat
from chat.utils.chat_consumer_helpers import (
    get_new_contacts_by_username,
    current_user_chat_data,
    make_new_chat,
    prepare_chat_data,
    prepare_chat_message,
)


User = get_user_model()


class FindNewContactsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        input_username = data["username"]

        contacts = await database_sync_to_async(
            get_new_contacts_by_username
        )(
            current_user=self.scope["user"],
            input_username=input_username
        )

        await self.send(text_data=json.dumps({"contacts": contacts}))


class ChatListConsumer(AsyncWebsocketConsumer):
    STATUSES = ("GET", "UPDATE")

    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        status_type = json.loads(text_data).get("type")

        if status_type in self.STATUSES:
            chat_data = await database_sync_to_async(
                current_user_chat_data
            )(
                user_id=self.scope["user"].id
            )

            await self.send(text_data=json.dumps({"chats": chat_data}))


class ChatCreateConsumer(AsyncWebsocketConsumer):
    STATUS = "CREATED"

    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        contact_username = data["contact"]

        await database_sync_to_async(
            make_new_chat
        )(
            current_user=self.scope["user"],
            contact_username=contact_username
        )
        await self.send(text_data=json.dumps({"status": self.STATUS}))


class ChatDetailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat = await self.get_chat()
        self.chat_group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

        chat_data = await database_sync_to_async(
            prepare_chat_data
        )(
            chat=self.chat,
            current_user=self.scope["user"]
        )

        await self.send(
            text_data=json.dumps(
                chat_data,
            )
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        chat_data = await database_sync_to_async(
            prepare_chat_message
        )(
            chat=self.chat,
            user=self.scope["user"],
            new_message=data["message"]
        )

        await self.channel_layer.group_send(
            self.chat_group_name,
            {"type": "chat.message", "chat_data": chat_data}
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def chat_message(self, event):
        chat_data = {"type": event["type"], **event["chat_data"]}

        await self.send(text_data=json.dumps(
            chat_data,
        ))

    @database_sync_to_async
    def get_chat(self):
        return Chat.objects.prefetch_related(
            "members", "messages", "messages__user"
        ).get(id=self.chat_id)
