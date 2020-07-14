import MySQLdb
from flask import current_app, _app_ctx_stack


class MySqlPool:
    config_prefix = ''

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)

    @property
    def connect(self):
        return MySQLdb.connect(
            host=current_app.config.get(f'{self.config_prefix}MYSQL_HOST'),
            port=current_app.config.get(f'{self.config_prefix}MYSQL_PORT'),
            user=current_app.config.get(f'{self.config_prefix}MYSQL_USER'),
            passwd=current_app.config.get(f'{self.config_prefix}MYSQL_PASSWORD'),
            db=current_app.config.get(f'{self.config_prefix}MYSQL_DB'),
        )

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


class Db(MySqlPool):
    pass


class SlaveDb(MySqlPool):
    config_prefix = 'SLAVE_'
