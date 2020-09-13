import pika
from flask import current_app, _app_ctx_stack


class AppBroker:

    connection_name = 'broker_connection'

    def init_app(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)

    @property
    def connection(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, self.connection_name):
                setattr(ctx, self.connection_name, self.connect)
            return getattr(ctx, self.connection_name)

    @property
    def connect(self):
        return pika.BlockingConnection(pika.URLParameters(current_app.config.get('MAIN_BROKER_URL')))

    @property
    def channel(self):
        return self.connection.channel()

    def publish(self, queue, body):
        with current_app.app_context():
            self.channel.queue_declare(queue=queue)
            self.channel.basic_publish(exchange='', routing_key=queue, body=body)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, self.connection_name):
            getattr(ctx, self.connection_name).close()
