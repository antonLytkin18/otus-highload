from abc import ABC, abstractmethod

from flask import current_app, _app_ctx_stack
from redis import StrictRedis


class DbConnectionPool(ABC):

    def init_app(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)

    @property
    def connection(self):
        ctx = _app_ctx_stack.top
        if ctx is None:
            return None
        if not hasattr(ctx, 'db_connection_pool'):
            ctx.db_connection_pool = {}
        connection_name = self.__class__.__name__
        if not ctx.db_connection_pool.get(connection_name, False):
            ctx.db_connection_pool[connection_name] = self.connect
        return ctx.db_connection_pool[connection_name]

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if not hasattr(ctx, 'db_connection_pool'):
            return
        for name, connection in ctx.db_connection_pool.items():
            connection.close()

    @abstractmethod
    def connect(self):
        pass


class RedisPool(DbConnectionPool):

    @property
    def connect(self):
        return StrictRedis(host=current_app.config.get('REDIS_CACHE_HOST'), decode_responses=True)


class RedisDb(RedisPool):
    pass
