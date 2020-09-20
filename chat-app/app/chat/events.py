import json
from datetime import datetime

from blinker import signal
from flask import current_app

from app.chat.gateways import CounterAppGateway
from app.db.models import User, ChatMessage, ChatMessageStatus
from app.db.repositories import UserRepository

user_registered = signal('user-registered')
chat_message_added = signal('chat-message-added')
chat_message_read = signal('chat-message-read')


@user_registered.connect
def register_user(ch, **kwargs):
    payload = json.loads(kwargs.get('body'))
    repository: UserRepository = current_app.injector.get(UserRepository)
    repository.save(User(
        id=payload['id'],
        name=payload['name'],
        last_name=payload['last_name']
    ))


@chat_message_added.connect
def set_not_read_message_status(chat_service, **kwargs):
    counter_gateway: CounterAppGateway = kwargs.get('counter_gateway')
    chat_message: ChatMessage = kwargs.get('chat_message')
    chat_message_status_repository = kwargs.get('chat_message_status_repository')

    for user_id in chat_service.find_participants(chat_message):
        chat_message_status = chat_message_status_repository.model_class(
            user_id=user_id,
            chat_message_id=chat_message.id,
            date_create=datetime.now()
        )
        chat_message_status.set_not_read_status()
        chat_message_status_repository.save(chat_message_status)

        if not counter_gateway.incr(chat_message.chat_id, user_id):
            chat_message_status.set_read_status()
            chat_message_status_repository.save(chat_message_status)


@chat_message_read.connect
def set_read_message_status(chat_service, **kwargs):
    counter_gateway: CounterAppGateway = kwargs.get('counter_gateway')
    chat_message: ChatMessage = kwargs.get('chat_message')
    chat_message_status: ChatMessageStatus = kwargs.get('chat_message_status')
    chat_message_status_repository = kwargs.get('chat_message_status_repository')

    if not counter_gateway.decr(chat_message.chat_id, chat_message_status.user_id):
        chat_message_status.set_not_read_status()
        chat_message_status_repository.save(chat_message_status)
