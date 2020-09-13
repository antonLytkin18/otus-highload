from flask import current_app
from flask_socketio import SocketIO


class AppSocketIO:

    def __init__(self):
        self.__connection = SocketIO(logger=True, message_queue=current_app.config.get('SOCKETIO_BROKER_URL'))

    @property
    def connection(self):
        return self.__connection
