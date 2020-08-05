from injector import singleton

from app.auth.services import RegistrationService
from app.chat.services import ChatService
from app.db.db import Db, SlaveDb, MySqlPool, ChatShardedDb
from app.follower.services import FollowerService
from app.db.repositories import UserRepository, UserFollowerRepository, FollowerRepository, \
    UserFollowerReadOnlyRepository


def configure(binder):
    binder.bind(RegistrationService, scope=singleton)
    binder.bind(FollowerService, scope=singleton)
    binder.bind(ChatService, scope=singleton)
    binder.bind(UserRepository, scope=singleton)
    binder.bind(UserFollowerRepository, scope=singleton)
    binder.bind(UserFollowerReadOnlyRepository, scope=singleton)
    binder.bind(FollowerRepository, scope=singleton)
    binder.bind(MySqlPool, to=Db, scope=singleton)
    binder.bind(Db, scope=singleton)
    binder.bind(SlaveDb, scope=singleton)
    binder.bind(ChatShardedDb, scope=singleton)
