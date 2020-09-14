from injector import singleton

from app.auth.services import RegistrationService
from app.broker.broker import AppBroker
from app.db.db import DbConnectionPool, Db, SlaveDb, ChatShardedDb, TarantoolDb, RedisDb
from app.feed.services import FeedService
from app.follower.services import FollowerService
from app.db.repositories import UserRepository, UserFollowerRepository, FollowerRepository, \
    UserFollowerReadOnlyRepository, UserTarantoolRepository, PostRepository, FeedRepository
from app.socketio.socketio import AppSocketIO


def configure(binder):
    binder.bind(RegistrationService, scope=singleton)
    binder.bind(FollowerService, scope=singleton)
    binder.bind(FeedService, scope=singleton)
    binder.bind(UserRepository, scope=singleton)
    binder.bind(UserFollowerRepository, scope=singleton)
    binder.bind(UserFollowerReadOnlyRepository, scope=singleton)
    binder.bind(FollowerRepository, scope=singleton)
    binder.bind(PostRepository, scope=singleton)
    binder.bind(FeedRepository, scope=singleton)
    binder.bind(DbConnectionPool, to=Db, scope=singleton)
    binder.bind(Db, scope=singleton)
    binder.bind(SlaveDb, scope=singleton)
    binder.bind(ChatShardedDb, scope=singleton)
    binder.bind(TarantoolDb, scope=singleton)
    binder.bind(RedisDb, scope=singleton)
    binder.bind(UserTarantoolRepository, scope=singleton)
    binder.bind(AppSocketIO, scope=singleton)
    binder.bind(AppBroker, scope=singleton)
