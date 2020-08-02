from dataclasses import dataclass
from datetime import datetime

from injector import inject

from app.db.models import Chat, ChatMessage
from app.db.repositories import ChatRepository, ChatMessageRepository, UserRepository


@dataclass()
class ChatMessageDTO:
    is_current_user: bool = False
    user_id: int = None
    user_name: str = None
    message: str = None
    date_create: str = None


@dataclass()
class ChatDTO:
    id: int = None
    user_id: int = None
    user_name: str = None
    last_message: ChatMessageDTO = None


class ChatService:

    @inject
    def __init__(self, user_repository: UserRepository, chat_repository: ChatRepository,
                 chat_message_repository: ChatMessageRepository
                 ):
        self.user_repository = user_repository
        self.chat_repository = chat_repository
        self.chat_message_repository = chat_message_repository

    def find_or_create_chat(self, from_user_id, to_user_id) -> Chat:
        chat = self.chat_repository.find_one(from_user_id=from_user_id, to_user_id=to_user_id)
        chat = chat or self.chat_repository.find_one(from_user_id=to_user_id, to_user_id=from_user_id)
        if chat:
            return chat
        chat = Chat(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            date_create=datetime.now()
        )
        self.chat_repository.save(chat)
        return chat

    def find_chats(self, user_id) -> list:
        result = []
        chats = self.chat_repository.find_all(from_user_id=user_id) + self.chat_repository.find_all(to_user_id=user_id)
        for chat in chats:
            user_to_id = chat.from_user_id if chat.from_user_id != user_id else chat.to_user_id
            user_to = self.user_repository.find_one(id=user_to_id)
            last_message = self.chat_message_repository.find_one(chat_id=chat.id, order_by='ID DESC')
            result.append(ChatDTO(
                id=chat.id,
                user_id=user_to_id,
                user_name=f'{user_to.last_name} {user_to.name}' if user_to else '',
                last_message=ChatMessageDTO(
                    message=last_message.message if last_message else '',
                    date_create=last_message.date_create.strftime('%d.%m.%Y, %H:%M') if last_message else ''
                ),
            ))

        return result

    def add_message(self, chat_id, user_id, message) -> ChatMessageDTO:
        message = ChatMessage(
            chat_id=chat_id,
            user_id=user_id,
            message=message,
            date_create=datetime.now()
        )
        self.chat_message_repository.save(message)
        user = self.user_repository.find_one(id=message.user_id)
        return ChatMessageDTO(
            is_current_user=True,
            user_id=message.user_id,
            user_name=f'{user.last_name} {user.name}' if user else '',
            message=message.message,
            date_create=message.date_create.strftime('%d.%m.%Y, %H:%M')
        )

    def find_messages(self, chat_id, user_id) -> list:
        result = []
        users_cached = {}
        messages = self.chat_message_repository.find_all(chat_id=chat_id)
        for message in messages:
            user = users_cached.get(user_id, False)
            if not user:
                user = self.user_repository.find_one(id=message.user_id)
                users_cached[user.id] = user
            result.append(ChatMessageDTO(
                is_current_user=user_id == user.id,
                user_id=user.id,
                user_name=f'{user.last_name} {user.name}' if user else '',
                message=message.message,
                date_create=message.date_create.strftime('%d.%m.%Y, %H:%M')
            ))
        return result
