from __future__ import annotations
from typing import List, Dict, Set

from django.contrib.auth import get_user_model

from chat.models import Chat, Message


User = get_user_model()


def get_new_contacts_by_username(
        current_user: User,
        input_username: str
) -> List[Dict[str, str | bool]]:
    excluded_ids = current_user_contacts_ids(user_id=current_user.id)
    excluded_ids.add(current_user.id)

    return [
        {
            "username": user.username,
            "is_online": user.is_online,
            "photo": user.photo.url
        }
        for user in
        User.objects.filter(
            username__icontains=input_username
        ).exclude(id__in=excluded_ids)
    ]


def current_user_contacts_ids(
        user_id: int
) -> Set[int]:
    current_user = user_prefetched_chats_members(user_id=user_id)

    return {
        user.id
        for chat in current_user.chats.all()
        for user in chat.members.all()
        if user.id != user_id
    }


def current_user_chat_data(
        user_id: int
) -> List[Dict[str, str | bool]]:
    current_user = user_prefetched_chats_members(user_id=user_id)

    return [
        {
            "username": user.username,
            "is_online": user.is_online,
            "chat_id": str(chat.id),
            "photo": user.photo.url
        }
        for chat in current_user.chats.all()
        for user in chat.members.all()
        if user.id != user_id
    ]


def user_prefetched_chats_members(
        user_id: int
) -> User:
    return User.objects.prefetch_related(
        "chats__members"
    ).get(id=user_id)


def chat_history(
        chat: Chat
) -> List[Dict[str, str]]:
    return [
        {
            "user": message.user.username,
            "text": message.text,
            "date": message.created_at.isoformat(),
            "photo": message.user.photo.url
        }
        for message in chat.messages.all()
    ]


def chat_title(
        chat: Chat,
        current_username: str
) -> str:
    return "Chat with " + "".join([
        member.username
        for member in chat.members.all()
        if member.username != current_username
    ])


def make_new_chat(
        current_user: User,
        contact_username: str
) -> None:
    chat = Chat()
    chat.save()

    contact = User.objects.get(username=contact_username)

    chat.members.add(current_user, contact)


def prepare_chat_data(
        chat: Chat,
        current_user: User
) -> Dict[str, str | List[Dict[str, str]] | int]:
    messages = chat_history(chat=chat)

    return {
        "title": chat_title(
            chat=chat,
            current_username=current_user.username
        ),
        "messages": messages,
        "quantity": len(messages)
    }


def create_chat_message(
        chat: Chat,
        user: User,
        new_message: str
) -> Message:
    return Message.objects.create(
        chat=chat,
        text=new_message,
        user=user
    )


def prepare_chat_message(
        chat: Chat,
        user: User,
        new_message: str
) -> Dict[str, str]:
    message = create_chat_message(
        chat=chat,
        user=user,
        new_message=new_message
    )
    return {
        "user": user.username,
        "text": message.text,
        "date": message.created_at.isoformat(),
        "photo": user.photo.url
    }
