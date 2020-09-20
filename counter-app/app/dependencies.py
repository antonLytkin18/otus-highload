from injector import singleton

from app.db.db import RedisDb
from app.db.repositories import ChatCounterRepository


def configure(binder):
    binder.bind(RedisDb, scope=singleton)
    binder.bind(ChatCounterRepository, scope=singleton)
