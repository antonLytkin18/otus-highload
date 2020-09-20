from dataclasses import dataclass
from datetime import datetime

from blinker import signal
from injector import inject

from app.chat.gateways import CounterAppGateway
from app.db.models import ChatMessage, User, Chat, ChatMessageStatus
from app.db.repositories import ChatRepository, ChatMessageRepository, UserRepository, ChatMessageStatusRepository


@dataclass()
class ChatMessageDTO:
    id: int = None
    is_current_user: bool = False
    user_id: int = None
    user_name: str = None
    message: str = None
    is_read: bool = None
    date_create: str = None


@dataclass()
class ChatDTO:
    id: int = None
    user_id: int = None
    user_name: str = None
    last_message: ChatMessageDTO = None
    unread_messages_count: int = None


class ChatService:

    @inject
    def __init__(self, user_repository: UserRepository, chat_repository: ChatRepository,
                 chat_message_repository: ChatMessageRepository,
                 chat_message_status_repository: ChatMessageStatusRepository, counter_gateway: CounterAppGateway):
        self.user_repository = user_repository
        self.chat_repository = chat_repository
        self.chat_message_repository = chat_message_repository
        self.chat_message_status_repository = chat_message_status_repository
        self.counter_gateway = counter_gateway

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
        count_items = self.counter_gateway.count_all(user_id)
        for chat in chats:
            user_to_id = chat.from_user_id if chat.from_user_id != user_id else chat.to_user_id
            user_to: User = self.user_repository.find_one(id=user_to_id)
            last_message = self.chat_message_repository.find_one(chat_id=chat.id, order_by='ID DESC')
            result.append(ChatDTO(
                id=chat.id,
                user_id=user_to_id,
                user_name=f'{user_to.last_name} {user_to.name}' if user_to else '',
                last_message=ChatMessageDTO(
                    message=last_message.message if last_message else '',
                    date_create=last_message.date_create.strftime('%d.%m.%Y, %H:%M') if last_message else '',
                ) if last_message else None,
                unread_messages_count=count_items.get(str(chat.id), None),
            ))

        return result

    def add_message(self, chat_id, user_id, message) -> ChatMessageDTO:
        message = ChatMessage(
            chat_id=chat_id,
            user_id=user_id,
            message=message,
            date_create=datetime.now()
        )
        if self.chat_message_repository.save(message):
            chat_message_added = signal('chat-message-added')
            chat_message_added.send(
                self,
                chat_message=message,
                chat_message_status_repository=self.chat_message_status_repository,
                counter_gateway=self.counter_gateway
            )

        user = self.user_repository.find_one(id=message.user_id)
        return ChatMessageDTO(
            is_current_user=True,
            user_id=message.user_id,
            user_name=f'{user.last_name} {user.name}' if user else '',
            message=message.message,
            date_create=message.date_create.strftime('%d.%m.%Y, %H:%M')
        )

    def read_message(self, message_id, user_id):
        chat_message_statuses = self.chat_message_status_repository.find_all(
            user_id=user_id,
            chat_message_id=message_id
        )
        for chat_message_status in chat_message_statuses:
            chat_message_status.set_read_status()
            if not self.chat_message_status_repository.save(chat_message_status):
                continue
            chat_message_read = signal('chat-message-read')
            chat_message_read.send(
                self,
                chat_message=self.chat_message_repository.find_one(id=message_id),
                chat_message_status=chat_message_status,
                chat_message_status_repository=self.chat_message_status_repository,
                counter_gateway=self.counter_gateway
            )

    def find_messages(self, chat_id, user_id) -> list:
        result = []
        users_cached = {}
        messages = self.chat_message_repository.find_all(chat_id=chat_id)
        for message in messages:
            user: User = users_cached.get(message.user_id, False)
            if not user:
                user = self.user_repository.find_one(id=message.user_id)
                users_cached[user.id] = user
            chat_message_status: ChatMessageStatus = self.chat_message_status_repository.find_one(
                chat_message_id=message.id
            )
            result.append(ChatMessageDTO(
                id=message.id,
                is_current_user=user_id == user.id,
                user_id=user.id,
                user_name=f'{user.last_name} {user.name}' if user else '',
                message=message.message,
                is_read=chat_message_status.is_read if chat_message_status else True,
                date_create=message.date_create.strftime('%d.%m.%Y, %H:%M')
            ))
        return result

    def find_participants(self, chat_message: ChatMessage) -> list:
        chat = self.chat_repository.find_one(id=chat_message.chat_id)
        if not chat:
            return []
        return [user_id for user_id in [chat.from_user_id, chat.to_user_id] if user_id != chat_message.user_id]
