from abc import ABC, abstractmethod

import MySQLdb
import tarantool
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


class MySqlPool(DbConnectionPool):
    config_prefix = ''

    @property
    def connect(self):
        return MySQLdb.connect(
            host=current_app.config.get(f'{self.config_prefix}MYSQL_HOST'),
            port=current_app.config.get(f'{self.config_prefix}MYSQL_PORT'),
            user=current_app.config.get(f'{self.config_prefix}MYSQL_USER'),
            passwd=current_app.config.get(f'{self.config_prefix}MYSQL_PASSWORD'),
            db=current_app.config.get(f'{self.config_prefix}MYSQL_DB'),
        )


class TarantoolPool(DbConnectionPool):

    @property
    def connect(self):
        return tarantool.connect(
            host=current_app.config.get('TARANTOOL_HOST'),
            port=current_app.config.get('TARANTOOL_PORT')
        )


class RedisPool(DbConnectionPool):

    @property
    def connect(self):
        return StrictRedis(host=current_app.config.get('REDIS_CACHE_HOST'), decode_responses=True)


class Db(MySqlPool):
    pass


class SlaveDb(MySqlPool):
    config_prefix = 'SLAVE_'


class ChatShardedDb(MySqlPool):
    config_prefix = 'CHAT_'


class TarantoolDb(TarantoolPool):
    pass


class RedisDb(RedisPool):
    pass
