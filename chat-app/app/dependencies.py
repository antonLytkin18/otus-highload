from injector import singleton

from app.chat.services import ChatService

from app.chat.gateways import CounterAppGateway
from app.db.db import DbConnectionPool, Db
from app.db.repositories import ChatRepository, ChatMessageRepository, ChatMessageStatusRepository, UserRepository


def configure(binder):
    binder.bind(DbConnectionPool, to=Db, scope=singleton)
    binder.bind(UserRepository, scope=singleton)
    binder.bind(ChatRepository, scope=singleton)
    binder.bind(ChatMessageRepository, scope=singleton)
    binder.bind(ChatMessageStatusRepository, scope=singleton)
    binder.bind(ChatService, scope=singleton)
    binder.bind(CounterAppGateway, scope=singleton)
