import pika

from app import create_app
from blinker import signal

app = create_app()


def init_broker_channel():
    connection = pika.BlockingConnection(pika.URLParameters(app.config.get('MAIN_BROKER_URL')))
    channel = connection.channel()
    init_queues(channel)
    return channel


def init_queues(channel):
    channel.queue_declare(queue='main-app-user-registered')
    channel.basic_consume('main-app-user-registered', main_app_user_registered, auto_ack=True)


def main_app_user_registered(ch, method, properties, body):
    with app.app_context():
        user_registered = signal('user-registered')
        user_registered.send(ch, method=method, properties=properties, body=body)


broker_channel = init_broker_channel()
